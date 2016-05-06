
import logging
from zope import interface, schema
from zope.interface import implements, alsoProvides

# Plone
from Products.CMFCore.utils import getToolByName

# z3c.form
from z3c.form import form, field, button, widget,term
from z3c.form.browser import checkbox
from z3c.form.interfaces import IFormLayer

# plone.z3cform
from plone.app.layout.viewlets import ViewletBase
from plone.z3cform.widget import singlecheckboxwidget_factory
from plone.z3cform.layout import FormWrapper, wrap_form
from plone.z3cform.interfaces import IWrappedForm

# Do not mix with Products.Five.browser.pagetemplatefile.ViewPageTemplateFile
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile as Zope3PageTemplateFile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile

# z3c.form Choice
from zope.schema.interfaces import IContextSourceBinder
from z3c.formwidget.query.interfaces import IQuerySource
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from gcommons.Core.lib.container import gcommons_aq_container

logger = logging.getLogger('gcommons.Journal.browser.articleassigneditor')


class Editors(object):
    implements(IQuerySource)

    def __init__(self, context):
        self.context = context
        # Grab list of editors from container (Journal, Conference, whatever)
        gccontainer = gcommons_aq_container(self.context)
        self.editors = gccontainer.getEditors()
        self.vocab= SimpleVocabulary.fromItems([(x.getProperty('fullname'),x.getId()) for x in self.editors])
    
    def __contains__(self, term):
        return self.vocab.__contains__(term)
        
    def __iter__(self):
        return self.vocab.__iter__()
    
    def __len__(self):
        return self.vocab.__len__()
    
    def getTerm(self, value):
        return self.vocab.getTerm(value)
    
    def getTermByToken(self, value):
        return self.vocab.getTermByToken(value)
    
    def search(self, query_string):
        return [v for v in self if query_string.lower() in v.value.lower()]


class EditorsBinder(object):
    implements(IContextSourceBinder)
    def __call__(self, context):
        return Editors(context)  

class IAssignEditor(interface.Interface):
    editors = schema.Choice(title=u'Editors',
        description=u'Who should be the Action Editor for the piece',
        source=EditorsBinder(),
        required=True)
    currenteditor = schema.TextLine(title=u'Current Action Editor',
        readonly = True,
        required = False)
    

#
# retrieve default ISBN value from isbn= if it is there in the request 
def defaultActionEditor(value):
    actioneditor = value.context.get_action_editor(memberObject=True)
    if actioneditor is None:
       return 'Unassigned'
    name = actioneditor.getProperty('fullname')
    if name is None:
        name = actioneditor.getId()
    return name

DefaultActionEditor = widget.ComputedWidgetAttribute(defaultActionEditor, field=IAssignEditor['currenteditor'])

class AssignEditorForm(form.Form):
    fields = field.Fields(IAssignEditor)
    ignoreContext = True # don't use context to get widget data
    label = u"Who should handle this piece?"
    prefix = "assignform."

    @button.buttonAndHandler(u'Assign', name='assign')
    def handleAssign(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        
        self.applyChanges(data)
        self.context.plone_utils.addPortalMessage(u'Action Editor registered.')
        view = self.context.getTypeInfo().getActionInfo('object/view', self.context)['url']
        self.request.response.redirect(view)

    def applyChanges(self, data):
        if data.get('editors') is not None:
            self.context.set_action_editor(data['editors'])

AssignEditorView = wrap_form(AssignEditorForm)

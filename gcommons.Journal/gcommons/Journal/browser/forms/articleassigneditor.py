
import logging
from zope import interface, schema
from zope.interface import implements, alsoProvides

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
from zope.app.pagetemplate import ViewPageTemplateFile as Zope3PageTemplateFile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile

# z3c.form Choice
from zope.schema.interfaces import IContextSourceBinder
from z3c.formwidget.query.interfaces import IQuerySource
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


logger = logging.getLogger('gcommons.Journal.browser.articleassigneditor')


class Editors(object):
    implements(IQuerySource)
    vocabulary = SimpleVocabulary((SimpleTerm(u'worldcat', 'WorldCat', u'John '),
				    SimpleTerm(u'wsdfaorldcat', 'VASSWorldCat', u'Roger Bacon')))

    def __init__(self, context):
        self.context = context

    __contains__ = vocabulary.__contains__
    __iter__ = vocabulary.__iter__
    getTerm = vocabulary.getTerm
    getTermByToken = vocabulary.getTermByToken

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
        logger.info("Data: %s" % data)
        
        self.context.plone_utils.addPortalMessage(u'Action Editor registered.')
        #view = self.context.getTypeInfo().getActionInfo('object/view', self.context)['url']
        #self.request.response.redirect(view)

    def applyChanges(self, data):
        self.context.storeVote(vote)

AssignEditorView = wrap_form(AssignEditorForm)


import logging
from zope import interface, schema
from zope.interface import implements
from z3c.form import form, field, button, widget,term
from plone.z3cform.layout import FormWrapper, wrap_form
from z3c.form.browser import checkbox
from plone.z3cform.widget import singlecheckboxwidget_factory

# Do not mix with Products.Five.browser.pagetemplatefile.ViewPageTemplateFile
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile as Zope3PageTemplateFile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile


logger = logging.getLogger('gcommons.Journal.browser.forms.editorsmeetingvote')


class EditorsMeetingPollVoteForm(form.Form):
    fields = None        # will get filled in on update()
    ignoreContext = True # don't use context to get widget data
    label = u"Indicate when you are available"
    prefix = "voteform."

    @button.buttonAndHandler(u'Vote!', name='vote')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        
        self.context.plone_utils.addPortalMessage(u'Vote registered.')
        view = self.context.getTypeInfo().getActionInfo('object/view', self.context)['url']
        self.request.response.redirect(view)

    def applyChanges(self, data):
        vote = []
        for key in data:
            itemid = int(key[len("option_"):])
            if data[key] is True:
                 vote.append(itemid)
        logger.info("Storing vote %s" % vote)
        self.context.storeVote(vote)
            
    def update(self):
        self.fields = field.Fields()

        n = 0
        pollOptions = self.context.getPollOptions()
        for itemId in pollOptions:
            fld =  schema.Bool(__name__ = "option_%d" % itemId,
                         title= u"%s - %s" % (pollOptions[itemId]['date'], pollOptions[itemId]['time']),
                         required=False,
                         default=False)
            self.fields += field.Fields(fld)
            n += 1

        for fld in self.fields:
            self.fields[fld].widgetFactory = singlecheckboxwidget_factory

        super(EditorsMeetingPollVoteForm,self).update()


VoteFormView = wrap_form(EditorsMeetingPollVoteForm)

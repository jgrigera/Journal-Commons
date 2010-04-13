from Acquisition import aq_inner
from OFS.SimpleItem import SimpleItem
from zope.component import adapts
from zope.component.interfaces import ComponentLookupError
from zope.interface import Interface, implements
from zope.formlib import form
from zope import schema

from plone.app.contentrules.browser.formhelper import AddForm, EditForm 
from plone.contentrules.rule.interfaces import IRuleElementData, IExecutable

from journalcommons.Utils import UtilsMessageFactory as _

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
import logging
logger = logging.getLogger('journalcommons.Utils.actions.newsmail')

# Python 2.5
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# Python 2.4
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Charset import Charset


class INewsMailAction(Interface):
    """Definition of the configuration available for a mail action
    """
    subject = schema.TextLine(title=_(u"Subject"),
                              description=_(u"Subject of the message"),
                              required=True)
    source = schema.TextLine(title=_(u"Email source"),
                             description=_("The email address that sends the email. If no email is provided here, it will use the portal from address."),
                             required=False)
    recipients = schema.TextLine(title=_(u"Email recipients"),
                                description=_("The email where you want to send this message. To send it to different email addresses, just separate them with a comma"),
                                required=True)
    message = schema.Text(title=_(u"Message"),
                          description=_(u"Type in here the message that you \
want to mail. Some defined content can be replaced: ${title} will be replaced \
by the title of the item. ${text} will be replaced with the content of the item. ${url} will be replaced by the URL of the item."),
                          required=True)


class NewsMailAction(SimpleItem):
    """
    The implementation of the action defined before
    """
    implements(INewsMailAction, IRuleElementData)

    subject = u''
    source = u''
    recipients = u''
    message = u''

    element = 'journalcommons.Utils.actions.NewsMail'

    @property
    def summary(self):
        return _(u"Email item to ${recipients}",
                 mapping=dict(recipients=self.recipients))


class NewsMailActionExecutor(object):
    """The executor for this action.
    """
    implements(IExecutable)
    adapts(Interface, INewsMailAction, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        recipients = [str(mail.strip()) for mail in \
                      self.element.recipients.split(',')]
        mailhost = getToolByName(aq_inner(self.context), "MailHost")
        if not mailhost:
            raise ComponentLookupError, 'You must have a Mailhost utility to execute this action'

        source = self.element.source
        urltool = getToolByName(aq_inner(self.context), "portal_url")
        portal = urltool.getPortalObject()
        email_charset = portal.getProperty('email_charset')
        if not source:
            # no source provided, looking for the site wide from email
            # address
            from_address = portal.getProperty('email_from_address')
            if not from_address:
                raise ValueError, 'You must provide a source address for this action or enter an email in the portal properties'
            from_name = portal.getProperty('email_from_name')
            source = "%s <%s>" % (from_name, from_address)

        obj = self.event.object
        event_title = safe_unicode(obj.Title())
        event_url = obj.absolute_url()
        event_text = safe_unicode(obj.getText())
        # TODO: awful. But this need to be in Ascii AFAIK, MIMEText dies on Unicode
        event_text = event_text.encode('ascii', 'replace')
        
        message_body = self.element.message.replace("${url}", event_url)
        message_body = message_body.replace("${title}", event_title)
        message_body = message_body.replace("${text}", event_text)
        
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        part1 = MIMEText("Please visit %s if you can't see the HTML version." % event_url, 'plain','utf-8')
        part2 = MIMEText(message_body, 'html')
        msg.attach(part1)
        msg.attach(part2)

        subject = self.element.subject.replace("${url}", event_url)
        subject = subject.replace("${title}", event_title)
        
        for email_recipient in recipients:
            # secureSend will be deprecated in Plone 4
            #mailhost.secureSend(msg.as_string(), email_recipient, source,
            #                    charset=email_charset, debug=False,
            #                    subtype='plain',
            #                    From=source)
            mailhost.send( msg.as_string(), mto=email_recipient, mfrom=source,
                                subject=subject)
        return True

class NewsMailAddForm(AddForm):
    """
    An add form for the mail action
    """
    form_fields = form.FormFields(INewsMailAction)
    label = _(u"Add Mail Item Action")
    description = _(u"Send the item by email to different recipient.")
    form_name = _(u"Configure element")

    def create(self, data):
        a = NewsMailAction()
        form.applyChanges(a, self.form_fields, data)
        return a

class NewsMailEditForm(EditForm):
    """
    An edit form for the mail action
    """
    form_fields = form.FormFields(INewsMailAction)
    label = _(u"Edit Mail Action")
    description = _(u"Send the item by email to different recipient.")
    form_name = _(u"Configure element")

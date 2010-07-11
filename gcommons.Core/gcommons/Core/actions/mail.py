

import logging
import re
from gcommons.Core.actions import Action
from Acquisition import aq_inner, aq_parent      

from Products.CMFCore.utils import getToolByName       
from Products.CMFPlone.utils import safe_unicode

# Python 2.5
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# Python 2.4
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Charset import Charset

 
logger = logging.getLogger('gcommons.Core.actions.mail')
            

class Values:
    """ helper for templating
    """
    def __init__(self):
        self.values = {}
    
    def set(self, name, value):
        self.values[name] = value
        
    def __getitem__(self, key):
        if self.values.has_key(key):
            return self.values[key]
        else:
            return "<TEMPLATE ERROR: undefined variable '%s'>" % key
                
RE_MATCH_SUBJECT = re.compile(u"\nSubject: ([^\n]+)")
RE_MATCH_TO = re.compile(u"\nTo: ([^\n]+)")


class mail(Action):
    
    def __init__(self, context=None, object=None, template=None):
        
        logger.info("Sending email due to configuration for item '%s'." % object.title)
        self.context = context
        self.object = object
        self.template = template

    def execute(self):

        portal_url = getToolByName(aq_inner(self.context), "portal_url")
        portal = portal_url.getPortalObject()
        mailhost = getToolByName(aq_inner(self.context), "MailHost")
        if not mailhost:
            raise ComponentLookupError, 'You must have a Mailhost utility to execute this action'

        # first construct all replacement variables
        values = Values()
        
        # the object
        values.set('title', safe_unicode(self.object.Title()))
        values.set('url', self.object.absolute_url())
                
        # user 
        user = self.context.portal_membership.getAuthenticatedMember()
        values.set('userid', user.getId())
        values.set('userfullname', user.fullname)
        values.set('useremail', user.email)
        
        values.set('date', 'TODO')
        
        email_text = safe_unicode(self.template % values)
        logger.info(email_text)
        
        # Parse template, extracting Subject and To
        match = RE_MATCH_SUBJECT.search(email_text)
        if match:
            email_subject = match.group(1)
        else:
            email_subject = safe_unicode(self.object.Title())
        email_text = RE_MATCH_SUBJECT.sub("", email_text)
        email_text = RE_MATCH_TO.sub("", email_text)


        # Now send the email        
        logger.info("1")
        logger.info(email_text)
        recipients = ["%s <%s>" % (user.fullname, user.email),]

        # Get From Address
        email_charset = portal.getProperty('email_charset')
        from_address = portal.getProperty('email_from_address')
        if not from_address:
            raise ValueError, 'You must provide a source address for this action or enter an email in the portal properties'
        from_name = portal.getProperty('email_from_name')
        source = "%s <%s>" % (from_name, from_address)


        for email_recipient in recipients:                         
                # Create message container - the correct MIME type is multipart/alternative.
                msg = MIMEMultipart('alternative')                                          
                msg['Subject'] = email_subject
                msg['From'] = source
                msg['To'] = email_recipient
                msg.preamble = 'This is a multi-part message in MIME format.'

                part1 = MIMEText(email_text, 'plain','utf-8')
                msg.attach(part1)
                # part2 = MIMEText(message_body, 'html')
                # msg.attach(part2)
                mailhost.send( msg.as_string() )
        return True
        
        
        

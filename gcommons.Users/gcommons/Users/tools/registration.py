import random
from smtplib import SMTPRecipientsRefused

from AccessControl import ClassSecurityInfo
from AccessControl import Unauthorized
from AccessControl.User import SpecialUser     
from Globals import InitializeClass

from Products.CMFCore.utils import getToolByName, _checkPermission
from Products.CMFPlone.RegistrationTool import RegistrationTool as BaseTool

from Products.remember.permissions import MAIL_PASSWORD_PERMISSION
from Products.remember.utils import trusted

# - remove '1', 'l', and 'I' to avoid confusion
# - remove '0', 'O', and 'Q' to avoid confusion
# - remove vowels to avoid spelling words
invalid_password_chars = ['a','e','i','o','u','y','l','q']

def getValidPasswordChars():
    password_chars = []
    for i in range(0, 26):
        if chr(ord('a')+i) not in invalid_password_chars:
            password_chars.append(chr(ord('a')+i))
            password_chars.append(chr(ord('A')+i))
    for i in range(2, 10):
        password_chars.append(chr(ord('0')+i))
    return password_chars

password_chars = getValidPasswordChars()


# seed the random number generator
random.seed()


class RegistrationTool(BaseTool):
    meta_type='remember Registration Tool'
    security = ClassSecurityInfo()

    security.declarePublic('testPasswordValidity')
    def testPasswordValidity(self, password, confirm=None):
        """ Verify that the password satisfies the portal's requirements.

        o If the password is valid, return None.
        o If not, return a string explaining why.

        Comparison of password and confirm handled in Member.post_validate.
        """
        if len(password) < 5 and not _checkPermission('Manage portal', self):
            return self.translate('help_password_creation',
                                  default='Passwords must contain at least ' +
                                          '5 characters.')
        if 'confirm_password' not in self.REQUEST.form:
            self.REQUEST.form['confirm_password'] = confirm
        errors = {}
        pm = getToolByName(self, 'portal_membership')
        user = pm.getAuthenticatedMember()
        if isinstance(user, SpecialUser):
            return None
        user.post_validate(self.REQUEST, errors)
        return errors.get('password')

    # A replacement for portal_registration's mailPassword function
    # The replacement secures the mail password function with
    # MAIL_PASSWORD_PERMISSION so that members can be disabled.
    security.declarePublic('mailPassword')
    def mailPassword(self, forgotten_userid, REQUEST, mail_template=None):
        """ Email a forgotten password to a member.
        
        o Raise an exception if user ID is not found.
        
        """
        membership = getToolByName(self, 'portal_membership')
        if not membership.checkPermission('Mail forgotten password', self):
            raise Unauthorized, "Mailing forgotten passwords has been disabled"

        utils = getToolByName(self, 'plone_utils')
        member = membership.getMemberById(forgotten_userid)

        if member is None:
            raise ValueError, 'The username you entered could not be found'

        try:
            email = member.getProperty('email')
        except Unauthorized:
            # probably a remember type
            if getattr(member.aq_base, 'getField', None) is None:
                raise ValueError, 'Unable to retrieve email address'
            field = member.getField('email')
            if field is None:
                raise ValueError, 'Unable to retrieve email address'
            email = field.getAccessor(member)()
            
        if not utils.validateSingleEmailAddress(email):
            raise ValueError, 'The email address did not validate'
        try:
            password = member.getPassword()
            reset_tool = getToolByName(self, 'portal_password_reset')
            reset = reset_tool.requestReset(forgotten_userid)
            email_charset = getattr(self, 'email_charset', 'UTF-8')
            if mail_template is None:
                mail_template = self.mail_password_template
            # members in private state can cause auth probs here,
            # wrap in priv escalation if necessary
            trusted_template = trusted(mail_template)
            mail_text = trusted_template(self,
                                         REQUEST,
                                         member=member,
                                         member_id=forgotten_userid,
                                         member_email=email,
                                         charset=email_charset,
                                         reset=reset)
            host = getToolByName(self, 'MailHost')
            
            if isinstance(mail_text, unicode):
                mail_text = mail_text.encode(email_charset)
            
            host.send(mail_text)
            return self.mail_password_response(self, REQUEST)

        except SMTPRecipientsRefused:
            # Don't disclose email address on failure
            raise SMTPRecipientsRefused('Recipient address rejected by server')


InitializeClass(RegistrationTool)

from zope.interface import implements, Interface
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize

# CORE
from journalcommons.Journal.browser import jcommonsView 
from Products.CMFCore.utils import getToolByName

from journalcommons.Journal import JournalMessageFactory as _
import logging
logger = logging.getLogger('journalcommons.Journal.browser.subissionsview')


class ISubmissionsView(Interface):
    """
    Submissions view interface
    """

    def get_your_articles():
        """ get list of articles"""


class SubmissionsView(jcommonsView):
    """
    Submissions browser view
    """
    implements(ISubmissionsView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        
        self.portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_your_articles(self):
        """
        This method returns all articles for currently logged in user
        """
        user = self.portal_membership.getAuthenticatedMember()
        user_id = user.getId()
        # maybe...
        #brains = self.context.listFolderContents(contentFilter={"portal_type" : "Article"})
        brains = self.portal_catalog({'portal_type': self.context.aq_getItemsType(),
                             'Creator': user_id,
                             'sort_on':'created',
                             'sort_order': 'reverse'})
        #                     'path':'/'.join(self.context.getPhysicalPath()),
        # TODO: search only in current journal
        return [i.getObject() for i in brains]
    
    """ Functions for login 'portlet'
    """
    def login_can_request_password(self):        
        return self.portal_membership.checkPermission('Mail forgotten password', self.context)

    def login_can_register(self):        
        if getToolByName(self.context, 'portal_registration', None) is None:            
            return False        
        return self.portal_membership.checkPermission('Add portal member', self.context)

    def login_form(self):        
        return '%s/login_form' % self.portal_state.portal_url()    
    
    def login_mail_password_form(self):        
        return '%s/mail_password_form' % self.portal_state.portal_url()
    
    def login_name(self):        
        auth = self.auth()        
        name = None        
        if auth is not None:            
            name = getattr(auth, 'name_cookie', None)        
        if not name:            
            name = '__ac_name'        
        return name    
    
    def login_password(self):        
        auth = self.auth()        
        passwd = None        
        if auth is not None:            
            passwd = getattr(auth, 'pw_cookie', None)        
        if not passwd:           
            passwd = '__ac_password'        
        return passwd

    
    @memoize    
    def auth(self, _marker=[]):        
        acl_users = getToolByName(self.context, 'acl_users')       
        return getattr(acl_users, 'credentials_cookie_auth', None)

    def join_form(self):
        return '%s/join_form' % self.portal_state.portal_url()    
        
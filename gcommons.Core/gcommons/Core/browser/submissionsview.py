from zope.interface import implements, Interface
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName

from gcommons.Core.browser import gcommonsView 

from gcommons.Core import CoreMessageFactory as _
import logging
logger = logging.getLogger('gcommons.Core.browser.submissionsview')


class ISubmissionsView(Interface):
    """
    Submissions view interface
    """

    def get_your_articles():
        """ get list of articles"""


class SubmissionsView(gcommonsView):
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

    """ List possible piece types here
    """
    def get_your_pieces(self, type):
        """
        This method returns all items of type 'type' for currently logged in user
        """
        user = self.portal_membership.getAuthenticatedMember()
        user_id = user.getId()
        
	brains = self.portal_catalog({'portal_type': type,
                             'getPrimaryAuthor': user_id,
                             'sort_on':'created',
                             'sort_order': 'reverse'})
        #                     'path':'/'.join(self.context.getPhysicalPath()),
        # TODO: search only in current journal
        return [i.getObject() for i in brains]
    
    def get_addable_items_list(self):
        return self.context.aq_getConfig().getItems()
        
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
        
    def get_enable_self_reg(self):
        # I should learn how to call plone.app.controlpanel.security, but this is a quick fix
        app_perms = self.portal.rolesOfPermission(permission='Add portal member')
        for appperm in app_perms: 
            if appperm['name'] == 'Anonymous' and \
               appperm['selected'] == 'SELECTED':
                return True
        return False

    
    @memoize    
    def auth(self, _marker=[]):        
        acl_users = getToolByName(self.context, 'acl_users')       
        return getattr(acl_users, 'credentials_cookie_auth', None)

    def join_form(self):
        return '%s/join_form' % self.portal_state.portal_url()    
        

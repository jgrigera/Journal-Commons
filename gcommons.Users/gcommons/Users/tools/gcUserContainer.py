
import logging
import StringIO

# Zope
from AccessControl import ClassSecurityInfo
from AccessControl.requestmethod import postonly       
from Globals import InitializeClass
from zope.interface import implements

# Plone
from Products.Archetypes import public as atapi
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs


# ??
from Products.CMFCore.interfaces import IMemberDataTool
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore import permissions as cmfcore_permissions
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.tools.memberdata import MemberDataTool as BaseTool

# gcommons
from gcommons.Users.interfaces import  IgcUserContainer
from gcommons.Users import UsersMessageFactory as _
from gcommons.Users.config import PROJECTNAME


logger = logging.getLogger("gcommons.Users.tools.gcUserContainer")


gcUserContainerSchema = atapi.BaseFolderSchema.copy() + atapi.Schema((

    # use MetadataStorage so as not to conflict w/ the 'description'
    # property used for old-school MemberData objects
    atapi.TextField(
        'description',
        default = 'Container for Members',
        widget = atapi.TextAreaWidget(rows = 5),
        ),
    ))

search_catalog = 'membrane_tool'


class gcUserContainer(atapi.BaseBTreeFolder, BaseTool):
    """Tool for gcommons Users."""
    """
    Default container for remember Member objects.  Members don't
    actually need to live here any more, but for BBB reasons we are
    still storing them here.
    """
    id = 'portal_gcommons_users'
    archetype_name = meta_type = portal_type = 'gcUserContainer'
    schema = gcUserContainerSchema
    toolicon = 'user.gif'

    implements(IgcUserContainer,
		IHideFromBreadcrumbs)    
    security = ClassSecurityInfo()

    manage_options=(
        {'label': 'Types', 'action': 'manage_membranetypes'},
        ) + atapi.BaseBTreeFolder.manage_options 

    filter_content_types = 1
    allowed_content_types = ['gcPerson',]
    global_allow = 0
    actions = ()
    aliases = {
       '(Default)': 'pre_edit_setup',
       'view': 'pre_edit_setup',
       'index.html': 'pre_edit_setup',
       'edit': 'pre_edit_setup',
       'base_view': 'pre_edit_setup'
    }   


    def __init__(self, **kwargs):
        atapi.BaseBTreeFolder.__init__(self, self.id, **kwargs)
        BaseTool.__init__(self)
        self.setTitle('gcommons Users')                                                                                                            
        self.unindexObject()                                                                                                                                            
                                                                                                                                                                        
    # tool should not appear in portal_catalog                                                                                                                          
    def at_post_edit_script(self):                                                                                                                                      
        self.unindexObject()                                                                                                                                            
        

    security.declareProtected(cmfcore_permissions.AddPortalMember, 'addMember')
    @postonly
    def addMember(self, id, password, roles=('JournalAuthor',), domains='',
                  properties=None, REQUEST=None):
        '''Creates a PortalMember and returns it. The properties argument
        can be a mapping with additional member properties. Raises an
        exception if the given id already exists, the password does not
        comply with the policy in effect, or the authenticated user is not
        allowed to grant one of the roles listed (where Member is a special
        role that can always be granted); these conditions should be
        detected before the fact so that a cleaner message can be printed.
        '''
        portal_registration = getToolByName(self, 'portal_registration')

        # XXX: this method violates the rules for tools/utilities:
        # it depends on a non-utility tool
        if not portal_registration.isMemberIdAllowed(id):
            raise ValueError(_(u'The login name you selected is already in '
                               u'use or is not valid. Please choose another.'))

        failMessage = portal_registration.testPasswordValidity(password)
        if failMessage is not None:
            raise ValueError(failMessage)

        if properties is not None:
            failMessage = portal_registration.testPropertiesValidity(properties)
            if failMessage is not None:
                raise ValueError(failMessage)

        # Limit the granted roles.
        # Anyone is always allowed to grant the 'Member' role.
        ##_limitGrantedRoles(roles, self, ('Member',))
        
        
        newid = self.invokeFactory('gcPerson', id, password=password) 
        member = getattr(self, newid)
        member.setPassword(password)

        # deal with name
        fullname = properties.get('fullname')
        firstName = fullname.split()[0]
        lastName = ' '.join(fullname.split()[1:])
        # Make sure this archetype is initialized
        data = {}
        schema = member.Schema()
        for f in schema._fields.values():
            if not f.required:
                continue
            
            if f.__name__ in [ "password", "id" ]:
                # Do not set password or member id
                continue
            
            # Autofill member field values
            if f.vocabulary:
                value = f.vocabulary[0][0]
            if f.__name__ in ['email',]:
                value = properties.get(f.__name__)
                
            
            if f.__name__ == 'firstName':
                value = firstName
            if f.__name__ == 'lastName':
                value = lastName

            data[f.__name__] = value
        member.update(**data)
        member.at_post_create_script()
        return member
    
    
    def migrateUsersToGCU(self):
        """
        Migrate existing users to gcPerson
        """
        out = StringIO.StringIO()
        portal_membership = getToolByName(self, 'portal_membership')
        for member in portal_membership.listMembers():
            login = member.getId()
            password = member.getPassword()
            properties={'username':member.getId(),'fullname':member.getProperty('fullname'),'email':member.getProperty('email')}
            logger.info( "%s|%s|%s|%s" % (login, properties['fullname'], properties['email'], password))
            print >> out, "%s|%s|%s|%s" % (login, member.getProperty('fullname'), member.getProperty('email'), password)
            portal_membership.deleteMembers([login,])
            
            if password is None:
                password = 'invalid'
            newmember = self.addMember(login, password, properties=properties)
            newmember.setPasswordDigested(password)
        return out.getvalue()
    



atapi.registerType(gcUserContainer, PROJECTNAME)
InitializeClass(gcUserContainer)

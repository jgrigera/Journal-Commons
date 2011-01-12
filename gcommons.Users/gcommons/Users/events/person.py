"""
Code stolen from FacultyStaffDirectory
"""
import logging
from Acquisition import aq_parent, aq_inner

from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IMembraneUserObject
# membrane 1.0 called this IUserRelated

logger = logging.getLogger("gcommons.Users.events.person")


def modifyPersonOwnership(event):
    """Let people own their own objects and modify their own user preferences.
    
    Stolen from Plone and CMF core, but made less picky about where users are 
    found. (and from borg, thanks, optilude!)
    """
    context = event.context

    catalog = getToolByName(context, 'portal_catalog')
    userId = IMembraneUserObject(context).getUserId()
    userFolder = getToolByName(context, 'acl_users')

    logger.info("Modifying ownership of %s" % userId)
    
    user = None
    while userFolder is not None:
        user = userFolder.getUserById(userId)
        if user is not None:
            break
        container = aq_parent(aq_inner(userFolder))
        parent = aq_parent(aq_inner(container))
        userFolder = getattr(parent, 'acl_users', None)
    
    if user is None:
        raise KeyError, "User %s cannot be found." % userId
    
    context.changeOwnership(user, False)

    def fixPersonRoles(context, userId):
        # Remove all other Owners of this Person object. Note that the creator will have an implicit
        # owner role. The User Preferences Editor role allows us to allow the user defined by the Person
        # to manage their own password and user preferences, but prevent the creator of the Person object
        # from modifying those fields.
        for owner in context.users_with_local_role('Owner'):
            roles = list(context.get_local_roles_for_userid(owner))
            roles.remove('Owner')
            if roles:
                context.manage_setLocalRoles(owner, roles)
            else:
                context.manage_delLocalRoles([owner])
                
        # Grant 'Owner' and 'User Preferences Editor' to the user defined by this object:
        roles = list(context.get_local_roles_for_userid(userId))
        roles.extend(['Owner', 'User Preferences Editor'])
        # eliminate duplicated roles
        roles = list(set(roles))
        context.manage_setLocalRoles(userId, roles)
        
    fixPersonRoles(context, user.getId())
    catalog.reindexObject(context)

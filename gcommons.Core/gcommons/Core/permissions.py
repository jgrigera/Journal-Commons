
from Products.CMFCore import permissions as CMFCorePermissions
from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles
from Products.CMFCore.permissions import View


class Roles:
	pass

roles = Roles()
roles.EditorialBoard = 'EditorialBoard'
roles.Author = 'JournalAuthor'

# Permissions
# Note these should be in sync with profiles/default/rolemap.xml
AddDraft = 'gcommons.Core: Add Draft'
AddComment = 'gcommons.Core: Add Comment'


SubmissionsViewOverview = 'gcommons.Core: SubmissionsFolder View Overview'



#security = ModuleSecurityInfo('gcommons.Core')
#security.declarePublic('MyPermission')
for newPermission in (SubmissionsViewOverview, ):
    setDefaultRoles(newPermission, ())


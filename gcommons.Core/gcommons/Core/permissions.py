
from Products.CMFCore import permissions as CMFCorePermissions
from AccessControl.SecurityInfo import ModuleSecurityInfo
from Products.CMFCore.permissions import setDefaultRoles
from Products.CMFCore.permissions import View


class Roles:
	pass

roles = Roles()
roles.EditorialBoard = 'EditorialBoard'
roles.Author = 'Authenticated'

# Permissions
# Note these should be in sync with profiles/default/rolemap.xml
AddDraft = 'gcommons.Core: Add Draft'
AddComment = 'gcommons.Core: Add Comment'
Vote = 'gcommons.Core: Vote'
SubmissionsViewOverview = 'gcommons.Core: SubmissionsFolder View Overview'
EditorsMeetingChangeDate = 'gcommons.Journal: EditorsMeeting Change Date'

#security = ModuleSecurityInfo('gcommons.Core')
#security.declarePublic('MyPermission')
for newPermission in (SubmissionsViewOverview, Vote, EditorsMeetingChangeDate):
    setDefaultRoles(newPermission, ())


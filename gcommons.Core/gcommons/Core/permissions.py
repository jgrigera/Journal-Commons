
from Products.CMFCore.permissions import View


class Roles:
	pass

roles = Roles()
roles.EditorialBoard = 'EditorialBoard'
roles.Author = 'JournalAuthor'

# Permissions
AddDraft = 'gcommons.Core: Add Draft'
AddComment = 'gcommons.Core: Add Comment'


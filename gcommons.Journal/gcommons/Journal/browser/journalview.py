
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from gcommons.Journal import JournalMessageFactory as _


class IJournalView(Interface):
    """
    JournalView view interface
    """

    def test():
        """ test method"""


class JournalView(BrowserView):
    """
    JournalView browser view
    """
    implements(IJournalView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def getFolderContents(self):
        brains = self.context.listFolderContents()
        return brains

    def debug_show_user_roles(self):
        portal_membership = getToolByName(self.context, 'portal_membership')
        user = portal_membership.getAuthenticatedMember()
        return 'Debug: Roles %s for %s' % (str(user.getRoles()), user.getId())

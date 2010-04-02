from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from journalcommons.Conference import ConferenceMessageFactory as _


class IConferenceView(Interface):
    """
    Conference view interface
    """

    def test():
        """ test method"""


class ConferenceView(BrowserView):
    """
    Conference browser view
    """
    implements(IConferenceView)

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

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from journalcommons.Journal import JournalMessageFactory as _


class IEditorsMeetingView(Interface):
    """
    Editors Meeting view interface
    """
    def getFolderContents():
        """ """


class EditorsMeetingView(BrowserView):
    """
    EditorsMeeting browser view
    """
    implements(IEditorsMeetingView)

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

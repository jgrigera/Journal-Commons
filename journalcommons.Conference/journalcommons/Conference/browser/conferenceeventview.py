from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from journalcommons.Conference import ConferenceMessageFactory as _


class IConferenceEventView(Interface):
    """
    ConferenceEvent view interface
    """
    def getEventPapers(self):
        pass


class ConferenceEventView(BrowserView):
    """
    ConferenceEvent browser view
    """
    implements(IConferenceEventView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def getEventPapers(self):
        return self.context.getBackReferences(relationship='refPanel')
        

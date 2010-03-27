from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from journalcommons.Journal import JournalMessageFactory as _


class IIssueView(Interface):
    """
    Issue view interface
    """



class IssueView(BrowserView):
    """
    IssueView browser view
    """
    implements(IIssueView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_sections(self):
        """
        This method returns all sections of this issue
        """
        brains = self.context.listFolderContents(contentFilter={"portal_type" : "Section"})
        return brains

    def get_section_articles(self, section):
        """
        This method returns all articles of this section
        """
        brains = section.listFolderContents(contentFilter={"portal_type" : "Article"})
        return brains

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from journalcommons.Journal import JournalMessageFactory as _


class ISubmissionsSearchView(Interface):
    """
    SubmissionsSearch view interface
    """
    def getSearchQueryString(request):
        """
        """


class SubmissionsSearchView(BrowserView):
    """
    SubmissionsSearch browser view
    """
    implements(ISubmissionsSearchView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def getSearchQueryString(self, request):
        """
        """
        return "TODO: submissionssearchview.py "

        
    def getFilteredSubmissions(self, request):
        kw = {}
        kw['state'] = request.get('state')
        kw['portal_type'] = request.get('portal_type')
        kw['get_item_subtype'] = request.get('get_item_subtype')
        kw['SearchableText'] = request.get('SearchableText')
        return self.context.searchSubmissions(**kw)

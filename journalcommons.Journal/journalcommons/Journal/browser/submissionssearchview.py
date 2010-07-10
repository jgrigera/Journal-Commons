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

    def getFilteredSubmissions(self,request):
        
        raise AttributeError("not implemented here")
#        submissions_search = { 
#             'portal_type': self.context.aq_config ... get items type(),
#             'sort_on':'created',
#             'sort_order': 'reverse',
#             'path': '/'.join(self.context.getPhysicalPath())
#        }
        state = request.get('state')
        if state is not None:
            submissions_search['review_state'] = state
        brains = self.portal_catalog(submissions_search)
        return brains


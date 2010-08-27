from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from gcommons.Journal import JournalMessageFactory as _


class IEditorsMeetingView(Interface):
    """
    Editors Meeting view interface
    """
    def getFolderContents():
        """ """

class IMeetingDraftsAsZipView(Interface):
    pass


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

    def readingListActions(self):
        results = []
        results.append( {   'url': 'gcommons_editorsmeeting_aszip_view', 
                            'icon':  'download_icon.gif',
                            'title':'Download all drafts',} )
        return results


class MeetingDraftsAsZipView(BrowserView):
    implements(IMeetingDraftsAsZipView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """
        This method gets called everytime the template needs to be rendered
        """
        self.request.RESPONSE.setHeader('Content-Type','application/zip')
        self.request.RESPONSE.addHeader("Content-Disposition","filename=%s.zip" % self.context.Title())
        self.request.RESPONSE.write( self.context.download_all_as_zip().getvalue() )
        return 
    

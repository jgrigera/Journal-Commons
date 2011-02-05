from zope.interface import implements, Interface


from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from gcommons.Core import permissions
from gcommons.Core.browser import gcommonsView
from gcommons.Journal import JournalMessageFactory as _


class IEditorsMeetingView(Interface):
    """
    Editors Meeting view interface
    """
    def getFolderContents():
        """ """

class IMeetingDraftsAsZipView(Interface):
    pass


class EditorsMeetingView(gcommonsView):
    """
    EditorsMeeting browser view
    """
    implements(IEditorsMeetingView)
    
    def getFolderContents(self):
        brains = self.context.listFolderContents()
        return brains

    def readingListActions(self):
        results = []
        results.append( {   'url': 'gcommons_editorsmeeting_aszip_view', 
                            'icon':  'download_icon.gif',
                            'title':'Download all drafts',} )
        return results
        
    def showEventDetails(self):
        # Dont show Event details unless Poll is closed
        if self.portal_workflow.getInfoFor(self.context, 'review_state') == 'closed':
            return True
        else:
            return False
    
    def isPollOpen(self):
        # checkPermission
        return self.portal_membership.checkPermission(permissions.Vote, self.context)
        
    def getTotalVotes(self, optionId):
    
        return 5

    



class MeetingDraftsAsZipView(BrowserView):
    implements(IMeetingDraftsAsZipView)

    def __call__(self):
        """
        This method gets called everytime the template needs to be rendered
        """
        self.request.RESPONSE.setHeader('Content-Type','application/zip')
        self.request.RESPONSE.addHeader("Content-Disposition","filename=%s.zip" % self.context.Title())
        self.request.RESPONSE.write( self.context.download_all_as_zip().getvalue() )
        return 
    

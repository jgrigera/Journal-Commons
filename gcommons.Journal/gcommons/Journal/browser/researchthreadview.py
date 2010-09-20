from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from gcommons.Journal import JournalMessageFactory as _

import logging
logger = logging.getLogger('gcommons.Journal')

class IresearchthreadView(Interface):
    """
    researchthread view interface
    """

    def test():
        """ test method"""

class researchthreadView(BrowserView):
    """
    researchthread browser view
    """
    implements(IresearchthreadView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def test(self):
        """
        test method
        """
        dummy = _(u'a dummy string')

        return {'dummy': dummy}

    def getEditors(self):
        editors = []
        oeditors = self.context.getEditors()
        for editor in oeditors:
            name = editor.getProperty('fullname')
            if name is None or name == "": 
                name = editor.getId()
            #TODO: proper href for gcUsers
            href = "%s/author/%s" % (self.portal.absolute_url(),editor.getId())
            editors.append({'fullname': name,
                            'url': href,
                            'bio': editor.getProperty('description')})
        return editors 

    def get_submissions_folders(self):
        """
        This method returns all articles of this section
        """
        brains = self.context.listFolderContents(contentFilter={"portal_type" : "SubmissionsFolder"})
        return brains

    def get_published_articles(self):
        """
        This method returns all articles of this section
        """
        brains = self.context.listFolderContents(contentFilter={"portal_type" : "Article"})
        return brains

logger.warning("test")

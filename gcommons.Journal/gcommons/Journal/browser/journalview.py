
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


import logging
logger = logging.getLogger('gcommons.Journal')

from zope.interface import implements, Interface
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from gcommons.Journal import JournalMessageFactory as _

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


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

    pt = ViewPageTemplateFile('templates/gc_rt_published_view.pt')
    pt_editor = ViewPageTemplateFile('templates/gc_researchthread_view.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """
        This method gets called everytime the template needs to be
        rendered. It sets templates for editors and others.
        """
        portal_membership = getToolByName(self.context, 'portal_membership')
        user = portal_membership.getAuthenticatedMember()
        user_id = user.getId()
        if self.is_editor(user_id):
            logger.info("user=%s is local editor!" % (user_id))
            return self.pt_editor()
        else:
            logger.info("user=%s not a local editor" % (user_id))
            # hide border from non local editors
            self.request.set('disable_border', True)
        return self.pt()

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def is_editor(self,id):
        """
        This method takes and id and returns true if id is local editor
        """
        oeditors = self.context.getEditors()
        for editor in oeditors:
            if id == editor.getId():
                return 1
        return None

    def getEditors(self):
        """
        This method returns all local editors
        """
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
                            'id:': editor.getId(),
                            'bio': editor.getProperty('description')})
        return editors 


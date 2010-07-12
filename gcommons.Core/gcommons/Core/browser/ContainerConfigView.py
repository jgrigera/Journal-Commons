from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode


from gcommons.Core import CoreMessageFactory as _


class IGCContainerConfigView(Interface):
    """
    gcommonsContainerConfig view interface
    """
    pass



class gcContainerConfigView(BrowserView):
    """
    browser view
    """
    implements(IGCContainerConfigView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_xml_config(self):
        return str(self.context.getConfiguration())

    
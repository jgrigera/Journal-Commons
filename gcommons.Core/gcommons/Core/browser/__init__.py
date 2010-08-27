#


from Products.Five import BrowserView

import logging
logger = logging.getLogger('gcommons.Core.browser.gcommonsView')




class gcommonsView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    def get_disable_border(self):
        """
        Let Plone display a border or not
        """
        if self.portal_membership.checkPermission('Modify Portal Content', self.context):
            return False
        return True

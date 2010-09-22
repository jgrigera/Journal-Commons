from DateTime import DateTime
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from gcommons.Core.lib.gctime import gcommons_userfriendly_date

from gcommons.Journal import JournalMessageFactory as _


class IgcfrontpageView(Interface):
    """
    gcfrontpage view interface
    """

    def test():
        """ test method"""


class gcfrontpageView(BrowserView):
    """
    gcfrontpage browser view
    """
    implements(IgcfrontpageView)

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

    def get_modification_date(self, content, full=False):
        modificationdate = content.ModificationDate()
        if full:
            return "%s (%s)" % (DateTime(modificationdate).strftime("%a %d %b %Y"),
                                gcommons_userfriendly_date(content.ModificationDate()))
        else:
            return "%s" % DateTime(modificationdate).strftime("%a %d %b %Y")

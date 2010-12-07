from zope.interface import implements, Interface

from Products.Five import BrowserView
from gcommons.Core.browser import gcommonsView 
from Products.CMFCore.utils import getToolByName

from journalcommons.Conference import ConferenceMessageFactory as _


class IConferencePaymentOverview(Interface):
    """
    ConferencePaymentOverview view interface
    """

    def test():
        """ test method"""


class ConferencePaymentOverview(gcommonsView):
    """
    ConferencePaymentOverview browser view
    """
    implements(IConferencePaymentOverview)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()


    def get_table_items(self):
        itemlist = self.context.getItems()
        items = {}
        for item in itemlist:
            items[ item['id'] ] = item
        # Sort items by id, extracting key before ':'
        itemids = items.keys() #[ a['id'] for a in itemlist ]
        itemids.sort(key=lambda x:x.split(':')[0])
        
        form = []
        for itemid in itemids:
            item = items[itemid]
           
            qty = len(self.context.filterTransactions(html=False,itemid=itemid))
            if int(item['price']) > 0:
                price = "$%s" % item['price']
                total = "$%d" % ( int(item['price']) * qty )
            else:
                price = ""
                total = ""
            
            form.append({'id':itemid, 'price': price, 'label':item ['name'], 
                         'description':item['description'], 'qty': qty, 'total': total })
        
        return form
    
    def get_total_transactions(self):
        return {'len':len(self.context._transactions()),
                'price':999}

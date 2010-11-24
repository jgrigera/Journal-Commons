"""Definition of the ConferencePayment content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

from Products.DataGridField.DataGridWidget import DataGridWidget
from Products.DataGridField.DataGridField import DataGridField

from journalcommons.Conference import ConferenceMessageFactory as _
from journalcommons.Conference.interfaces import IConferencePayment
from journalcommons.Conference.config import PROJECTNAME
from cStringIO import StringIO
from AccessControl import ClassSecurityInfo
import logging

logger = logging.getLogger('journalcommons.Conference.content.conferencepayment')


ConferencePaymentSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
   atapi.TextField(                                                                                                                                                    
        name='helpText',                                                                                                                                                
        allowable_content_types=('text/plain', 'text/structured', 'text/html',                                                                                          
                                 'application/msword'),                                                                                                                 
        widget=atapi.RichWidget(                                                                                                                                        
            label="Help text",                                                                                                                                          
            description="Enter any introductory help text you'd like to display on the tracker front page.",                                                            
            label_msgid='gcommons_label_helpText',                                                                                                                      
            description_msgid='gcommons_help_helpText',                                                                                                                 
            i18n_domain='gcommons.Core',                                                                                                                                
        ),                                                                                                                                                              
        default_output_type='text/html',                                                                                                                                
        searchable=True,                                                                                                                                                
        default="""
        <h3>Payment system</h3>
        """
    ),
        
    DataGridField(
        name='items',
        widget=DataGridWidget(
            label=_("Items"),
            description = _('Take your time to fill in the items that will be billed. For radio buttons use same id plus colon (see help).'),
            column_names=('Id', 'Name', 'Description', 'Price'),
        ),
        allow_empty_rows=False,
        required=False,
        columns=('id', 'name', 'description', 'price')
    ),

))


def finalizeConferencePaymentSchema(schema):
    schema['title'].storage = atapi.AnnotationStorage()
    schema['description'].storage = atapi.AnnotationStorage()
    schemata.finalizeATCTSchema(schema, moveDiscussion=False)
    return schema


class TransactionItem:
    def __init__(self):
        pass

class Transaction:
    """ A class to store Transactions
        here we store 
            a. what has been payed
            b. who has payed
            c. how (i.e. paypal or whatever data)
    """
    def __init__(self, context=None, items=None, userid=None):
        self._items = items
        self._context = context
        self._payed = False
        self._userid = userid
        
        # Get unique id
        generator = getToolByName(context, 'portal_uidgenerator')
        uid = generator()
        self._id = generator.convert(uid)   # this returns an integer
    
    def id(self):
        return self._id
    
    """ What (items)
    """
    def items(self):
        return self._items
    
    def total(self):
        _total = 0
        for i in self._items:
            _total = _total + int( i['price'] )
        return _total
    
    def description(self):
        return "Payment for %s (%s)" % (self._context.Title(),';'.join([i['name'] for i in self._items]))
    
    """ Who
    """
    def userid(self):
        return self._userid
    
    """ How (paypal)
    """
    def beenpayed(self):
        self._payed = True

    def handlePayback(self,authcode=None):
        pass 


    


class ConferencePayment(base.ATCTContent):
    """Registration and payment for conference"""
    implements(IConferencePayment)
    security = ClassSecurityInfo()

    meta_type = "ConferencePayment"
    schema = finalizeConferencePaymentSchema(ConferencePaymentSchema)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    
    """
    Transactions
    This will move to a tool/singleton
    """
    transactions = {}
        
    def listTransactions(self):
        out = StringIO()
        '\n'.join( [str(i) for i in self.transactions.values()] )
        return out.getvalue()
    
    def addTransaction(self, context=None, items=None, userid=None):
        transaction = Transaction( context, items, userid)
        self.transactions[transaction.id()] = transaction
        return transaction
    
    security.declarePublic('payback')
    def payback(self):
        """
        Paypal payback interface
        """
        request = getattr(self, "REQUEST", None)
        if request is None:
            return
        
        for e in ('AUTHCODE','AVSDATA','HOSTCODE','PNREF','RESPMSG','RESULT','INVOICENO'):
            logger.info("%s = %s" % (e,request.get(e)))
            
        try:
            transaction = self.transactions[id]
            transaction.handlePayback(authcode=request.get('AUTHCODE'))
        except KeyError:
            logger.error("PAYMENT ERROR: payment with no invoiceid???\n%s" % request)

    



atapi.registerType(ConferencePayment, PROJECTNAME)

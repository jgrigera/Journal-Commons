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
transactionlogger = logging.getLogger('gcommons.PayPal')

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
        self._paypaltr = None
        self._paypalref = None
        
        # Get unique id
        generator = getToolByName(context, 'portal_uidgenerator')
        uid = generator()
        self._id = generator.convert(uid)   # this returns an integer
    
    def id(self):
        return self._id
    
    def __str__(self):
        return "%s,%s,%s,%s,%s,%s" % (self._id,self._userid,self._payed,self._paypalref, self.total(), 
                                 '/'.join([i['name'] for i in self._items]) )
    
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
    def handlePayback(self,paypalref,paypaltr):
        self._paypaltr = paypaltr
        self._paypalref = paypalref
        self._payed = True


    


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
    This will be moved to a tool/singleton
    """
    def _transactions(self):
        try:
            if self.transactions is None:
                self.transactions = {}
        except AttributeError:
            self.transactions = {}            
        return self.transactions
    
        
    def listTransactions(self):
        """ Temp function to return CSV of all transactions
        """
        out = StringIO()
        out.write("id,userid,payed?,paypalref,total,items\n")
        out.write('\n'.join( [str(i) for i in self._transactions().values()] ))
        return out.getvalue()
    
    def addTransaction(self, context=None, items=None, userid=None):
        transaction = Transaction( context, items, userid)
        self._transactions()[transaction.id()] = transaction
        # Let ZODB know we changed
        self._p_changed = 1
        return transaction
    
    security.declarePublic('payback')
    def payback(self):
        """
        Paypal payback interface
        """
        request = getattr(self, "REQUEST", None)
        if request is None:
            return
        
        result = request.get('RESULT')
        paypalref = request.get('PNREF')
        if int(result) != 0:
            logger.warning("%s Payment declined" % paypalref)
            
        logger.info("PAYPAL %s Payment received" % paypalref)
        
        transactionlogger.info("---PAYPAL BEGIN---")
        for i in request.keys():
            transactionlogger.info("%s: %s" % (i, request.get(i)))
        transactionlogger.info("---PAYPAL END---")            
        try:
            paypaltr = {}
            for e in ('ADDRESS','ADDRESSTOSHIP','AMOUNT','AUTHCODE','AVSDATA','CITY','CITYTOSHIP',
                'COUNTRY','COUNTRYTOSHIP','CUSTID','DESCRIPTION','EMAIL','EMAILTOSHIP','FAX','FAXTOSHIP',
                'HOSTCODE','INVOICE','METHOD','NAME','NAMETOSHIP','PHONE','PHONETOSHIP','PNREF',
                'PONUM','RESPMSG','RESULT','STATE','STATETOSHIP','TAX','TYPE','USER1','ZIP','ZIPTOSHIP'):
                paypaltr[e] = request.get(e)
                logger.debug("%s = %s" % (e,request.get(e)))

            transactionid = int(request.get('INVOICE'))
            transaction = self._transactions()[transactionid]
            transaction.handlePayback(paypalref,paypaltr)
            # Let ZODB know we changed
            self._p_changed = 1
        except KeyError, e:
            logger.error("PAYMENT ERROR: cant find invoice %s\n%s\n%s" % (transactionid,e,request))

    



atapi.registerType(ConferencePayment, PROJECTNAME)

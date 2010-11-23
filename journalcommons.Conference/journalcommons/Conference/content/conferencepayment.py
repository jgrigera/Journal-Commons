"""Definition of the ConferencePayment content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from Products.DataGridField.DataGridWidget import DataGridWidget
from Products.DataGridField.DataGridField import DataGridField

from journalcommons.Conference import ConferenceMessageFactory as _
from journalcommons.Conference.interfaces import IConferencePayment
from journalcommons.Conference.config import PROJECTNAME
from cStringIO import StringIO
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


class Invoice:
    """ A class to store Invoices
    """
    def __init__(self,items):
        self._items = items
        self._id = 10
        self._payed = False
    
    def id(self):
        return self._id

    def payed(self):
        self._payed = True

class InvoiceItem:
    def __init__(self):
        pass
    


class ConferencePayment(base.ATCTContent):
    """Registration and payment for conference"""
    implements(IConferencePayment)

    meta_type = "ConferencePayment"
    schema = finalizeConferencePaymentSchema(ConferencePaymentSchema)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    
    """
    Invoices
    """
    invoices = {}
        
    def listInvoices(self):
        out = StringIO()
        '\n'.join( [str(i) for i in self.invoices.values()] )
        return out.getvalue()
    
    def addInvoice(self, items):
        invoice = Invoice(items)
        self.invoices[invoice.id()] = invoice
        return invoice
    
    def payInvoice(self, id):
        self.invoices[id].payed()
    
    
    def payback(self, **kwargs):
        """
        Paypal payback interface
        """
        logger.info("payback: %s" % kwargs)
        for e in ('AUTHCODE','AVSDATA','HOSTCODE','PNREF','RESPMSG','RESULT'):
            logger.info("%s = %s" % (e,kwargs.get(e)))
         

    



atapi.registerType(ConferencePayment, PROJECTNAME)

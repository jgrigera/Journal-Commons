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



class ConferencePayment(base.ATCTContent):
    """Registration and payment for conference"""
    implements(IConferencePayment)

    meta_type = "ConferencePayment"
    schema = finalizeConferencePaymentSchema(ConferencePaymentSchema)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    



atapi.registerType(ConferencePayment, PROJECTNAME)



import logging
from zope.interface import implements, directlyProvides
from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from journalcommons.Core.interfaces import IjcommonsEvent

# Event support
from DateTime import DateTime
from Products.ATContentTypes.utils import DT2dt
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin
from Products.ATContentTypes.interfaces import ICalendarSupport

import logging

logger = logging.getLogger('jcommons.Core.lib.jcommonsEventMixin')


"""
Mixin Schema with basic event fields
"""
jcommonsEventMixinSchema = atapi.Schema((

    atapi.StringField(
        name='venue',
        required=False,
        searchable=1,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Venue"),
            description=_(u"Description of the venue(s)"),
        ),
    ),

    #
    # Dates
    atapi.DateTimeField(
        name='startDate',                  
        required=True,                  
        searchable=False,                  
        accessor='start',                  
#TODO                  write_permission = ChangeEvents,                  
        default_method=DateTime,                  
        languageIndependent=True,                  
        widget = atapi.CalendarWidget(                        
                  description= '',                        
                  label=_(u'label_event_start', 
                          default=u'Event Starts')          
        ),
    ),    
    atapi.DateTimeField('endDate',                  
        required=True,                  
        searchable=False,                  
        accessor='end',                  
#TODO                        
#        write_permission = ChangeEvents,                  
        default_method=DateTime,                 
        languageIndependent=True,                  
        widget = atapi.CalendarWidget(                        
                description = '',                        
                label = _(u'label_event_end', default=u'Event Ends')
        ),
    ),
    

    # Computed
    atapi.ComputedField('start_date',        
        searchable=1,        
        expression='context._start_date()',       
    ),
    atapi.ComputedField('end_date',        
        searchable=1,        
        expression='context._end_date()',       
    ),
    atapi.ComputedField('duration',        
        searchable=1,        
        expression='context._duration()',       
    ),


    # Contact information
    atapi.StringField('contactName',                
                required=False,                
                searchable=True,                
                accessor='contact_name',
#                write_permission = ChangeEvents,               
                widget = atapi.StringWidget(                        
                                      description = '',                        
                                      label = _(u'label_contact_name', 
                                                default=u'Contact Name')                        
    )),    
                
    atapi.StringField('contactEmail',                
                required=False,                
                searchable=True,                
                accessor='contact_email',
#                write_permission = ChangeEvents,                
                validators = ('isEmail',),                
                widget = atapi.StringWidget(                       
                            description = '',                       
                            label = _(u'label_contact_email', 
                                      default=u'Contact E-mail')                        
                )
    ),    

    atapi.StringField('contactPhone',                
                required=False,                
                searchable=True,               
                accessor='contact_phone',
#                write_permission = ChangeEvents,                
                validators= (),                
                widget = atapi.StringWidget(                        
                              description = '',                        
                              label = _(u'label_contact_phone', 
                                        default=u'Contact Phone')                        
                )
    ),
    
))


class jcommonsEventMixin(CalendarSupportMixin):
    """Mixin for any item that can be represented as an Event, much like ATContentTypes Event"""
    implements(IjcommonsEvent)

    def getEventType(self):
        """
        """
        logger.info("UNIMPLEMENTED: Should implement getEventType(), not let this bad default run")
        return "jcommons Event"

        
    def event_url(self):
        """
        URL for ics or vcs, That is ourselves...
        """
        return self.absolute_url()
    

    """
    Helpers for computed fields
    """
    def _start_date(self):
        value = self['startDate']
        if value is None:
            value = self['creation_date']
        return DT2dt(value)

    def _end_date(self):
        value = self['endDate']
        if value is None:
            return self.start_date
        return DT2dt(value)

    def _duration(self):
        return self.end_date - self.start_date
    
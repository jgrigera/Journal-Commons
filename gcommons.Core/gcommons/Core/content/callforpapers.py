"""Definition of the CallForPapers content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

# Event support
from DateTime import DateTime
from Products.ATContentTypes.utils import DT2dt
from Products.ATContentTypes.utils import toSeconds
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin
from Products.ATContentTypes.interfaces import ICalendarSupport
from Products.ATContentTypes.interfaces import ICalendarSupport


from gcommons.Core import CoreMessageFactory as _
from gcommons.Core.interfaces import ICallForPapers
from gcommons.Core.config import PROJECTNAME

CallForPapersSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

  atapi.TextField('body',
            searchable = 1,
            required = 1,
            allowable_content_types = ('text/plain',
                                       'text/structured',
                                       'text/html',),
            default_output_type = 'text/x-html-safe',
            widget = atapi.RichWidget(label = _(u'Call text')),
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
                  label=_(u'label_call_start', 
                          default=u'Call Starts')          
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
                label = _(u'label_call_end', default=u'Call Ends')
        ),
    ),
    
    atapi.ComputedField('start_date',        
        searchable=1,        
        expression='context._start_date()',       
    ),
    atapi.ComputedField('end_date',        
        searchable=1,        
        expression='context._end_date()',       
    ),
    atapi.ComputedField('duration_total_days',
        searchable=1,        
        expression='context._duration_total_days()',
        accessor='total_days',                
    ),
    atapi.ComputedField('duration_months',
        searchable=1,        
        expression='context._duration_months()',       
    ),
    atapi.ComputedField('duration_days',
        searchable=1,        
        expression='context._duration_days()',       
    ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

CallForPapersSchema['title'].storage = atapi.AnnotationStorage()
CallForPapersSchema['description'].storage = atapi.AnnotationStorage()
CallForPapersSchema['body'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    CallForPapersSchema,
    folderish=False,
    moveDiscussion=False
)

class CallForPapers(base.ATCTContent,CalendarSupportMixin):
    """Call for papers"""
    implements(ICallForPapers)

    meta_type = "CallForPapers"
    schema = CallForPapersSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    body = atapi.ATFieldProperty('body')    

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    # Helpers for Computed Fields
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

    def _duration_total_days(self):
        return self.end().__sub__(self.start())

    def _duration_months(self):
        return int(self.total_days() / 30)

    def _duration_days(self):
        return int(self.total_days() - int(self.total_days() / 30) * 30)
 
    """ Helpers to share interface with Events
    """
    def getEventType(self):
        return ("CallForPapers",)
    
    def event_url(self):
        return self.absolute_url()

atapi.registerType(CallForPapers, PROJECTNAME)

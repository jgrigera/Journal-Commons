"""Definition of the Conference content type
"""

from zope.interface import implements, directlyProvides

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ModifyPortalContent, View

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from journalcommons.Conference import ConferenceMessageFactory as _
from journalcommons.Conference.interfaces import IConference
from journalcommons.Conference.config import PROJECTNAME

# Event support
from DateTime import DateTime
from Products.ATContentTypes.utils import DT2dt
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin
from Products.ATContentTypes.interfaces import ICalendarSupport



ConferenceSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        name='venue',
        required=False,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Venue"),
            description=_(u"Description of the venue(s)"),
        ),
    ),

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
    
    atapi.ComputedField('start_date',        
        searchable=1,        
        expression='context._start_date()',       
    ),
    atapi.ComputedField('end_date',        
        searchable=1,        
        expression='context._end_date()',       
    ),

))
"""
atapi.ComputedField('duration',        
    searchable=1,        
    expression='context._duration()',       
),
"""

                                                
                                                 
# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.
def finalizeConferenceSchema(schema):
    schema['title'].storage = atapi.AnnotationStorage()
    schema['description'].storage = atapi.AnnotationStorage()

    # Call ATContentTypes
    schemata.finalizeATCTSchema(
        schema,
        folderish=True,
        moveDiscussion=False
    )
    
    # finalizeATCTSchema moves 'location' into 'categories', we move it back to default
    schema.changeSchemataForField('location', 'default')
    schema.moveField('location', before='startDate')
    return schema


class Conference(folder.ATFolder,CalendarSupportMixin):
    """A container for the Conference"""
    #implements(IConference,ICalendarSupport)
    implements(IConference)

    meta_type = "Conference"
    schema = finalizeConferenceSchema(ConferenceSchema)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    security       = ClassSecurityInfo()

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

    def _duration(self):
        return self.end_date - self.start_date

    """
    Items to share with jcommons
    """
    def aq_getContainerName(self):
        return "Conference"
    def aq_getItemsName(self):
        return "Conference Paper"
    def aq_getItemsType(self):
        return "ConferencePaper"
    def aq_stateDraftsAllowed(self):
        return False
    
    def at_post_create_script(self):
        """ Create a folder for Submissions
        """
        fldid = self.invokeFactory('SubmissionsFolder', 'submit', title = 'Submissions',
                        description='This folder holds paper submissions')





atapi.registerType(Conference, PROJECTNAME)

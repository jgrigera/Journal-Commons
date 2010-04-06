"""Definition of the Conference content type
"""

from zope.interface import implements, directlyProvides

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ModifyPortalContent, View

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from journalcommons.Journal import JournalMessageFactory as _
from journalcommons.Journal.interfaces import IEditorsMeeting
from journalcommons.Journal.config import PROJECTNAME

# Event support
from DateTime import DateTime
from Products.ATContentTypes.utils import DT2dt
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin
from Products.ATContentTypes.interfaces import ICalendarSupport



EditorsMeetingSchema = folder.ATFolderSchema.copy() + atapi.Schema((
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
"""
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
                )),    
    
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
                )),
"""

))

"""
"""

                                                
                                                 
# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.
def finalizeEditorsMeetingSchema(schema):
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


class EditorsMeeting(folder.ATFolder,CalendarSupportMixin):
    """A place to store activity done during Editor's meeting"""
    #implements(IConference,ICalendarSupport)
    implements(IEditorsMeeting)

    meta_type = "EditorsMeeting"
    schema = finalizeEditorsMeetingSchema(EditorsMeetingSchema)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    venue = atapi.ATFieldProperty('venue')

    security       = ClassSecurityInfo()

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    
    # Helpers for Computed Fields
    # TODO end=start, maybe we could ask for hour duration?
    def end(self):
        return self['startDate']
        
    def _start_date(self):
        value = self['startDate']
        if value is None:
            value = self['creation_date']
        return DT2dt(value)

    def _end_date(self):
        value = self['startDate']
        if value is None:
            return self.start_date
        return DT2dt(value)

    def _duration(self):
        return self.end_date - self.start_date
    
    """ Helpers to share interface with Events (and thus use vcs_view, ics_view et.al.)
    """
    def getEventType(self):
        return ("Editors Meeting",)
    
    def event_url(self):
        return self.absolute_url()
    

atapi.registerType(EditorsMeeting, PROJECTNAME)

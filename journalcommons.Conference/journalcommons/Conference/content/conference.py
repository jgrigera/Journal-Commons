"""Definition of the Conference content type
"""

import os
import logging
from zope.interface import implements, directlyProvides
from Acquisition import aq_inner
from AccessControl import ClassSecurityInfo

from Products.CMFCore.permissions import ModifyPortalContent, View
from Products.CMFCore.utils import getToolByName
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# gcommons.Core
from gcommons.Core.lib.container import gcContainerMixin

# gcommons.Conference
from journalcommons.Conference import ConferenceMessageFactory as _
from journalcommons.Conference.interfaces import IConference
from journalcommons.Conference.config import PROJECTNAME

# Event support
from DateTime import DateTime
from Products.ATContentTypes.utils import DT2dt
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin
from Products.ATContentTypes.interfaces import ICalendarSupport

logger = logging.getLogger('gcommons.Conference.content.Conference')


                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                                                                  
ConferenceSchema = folder.ATFolderSchema.copy() + gcContainerMixin.schema.copy() + atapi.Schema((
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


    # Contact information
    atapi.StringField('contactName',                
                required=False,                
                searchable=True,                
                accessor='contact_name',
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
    
))
                                      
                                                 
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


class Conference(gcContainerMixin,folder.ATFolder,CalendarSupportMixin):
    """A container for the Conference"""
    #implements(IConference,ICalendarSupport)
    implements(IConference)

    meta_type = "Conference"
    schema = finalizeConferenceSchema(ConferenceSchema)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    venue = atapi.ATFieldProperty('venue')
    configuration = atapi.ATFieldProperty('configuration')

    security       = ClassSecurityInfo()

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
    
    """ Helpers to share interface with Events
    """
    def getEventType(self):
        return ("Conference",)
    
    def event_url(self):
        return self.absolute_url()
    

    def aq_getAvailablePanels(self):
        context = aq_inner(self)
        portal_catalog = getToolByName(context, 'portal_catalog')
        brains = portal_catalog({
                    'portal_type':'ConferenceEvent',
                    'path':'/'.join(context.getPhysicalPath()),
                    'sort_on':'getObjPositionInParent'})
        items = []
        for obj in brains:
            items.append(dict(                
                    path = obj.getURL(),                
                    title = obj.pretty_title_or_id(),   
                    uid = obj.UID,             
                    description = obj.Description,                
                    creator = obj.Creator,                
#                    review_state = obj.review_state,                
#                    review_state_class = 'state-%s ' % norm(obj.review_state),                
#                    mod_date = toLocalizedTime(obj.ModificationDate),
            ))
        return items



atapi.registerType(Conference, PROJECTNAME)

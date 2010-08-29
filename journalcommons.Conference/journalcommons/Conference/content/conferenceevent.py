"""Definition of the ConferenceEvent content type
"""

from zope.interface import implements, directlyProvides
from Acquisition import aq_inner

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.DataGridField.DataGridWidget import DataGridWidget
from Products.DataGridField.DataGridField import DataGridField
from gcommons.Core.widgets.SelectDescriptionWidget import SelectDescriptionWidget
#from journalcommons.Conference.permission import ChangeConferenceSchedule

# Event support
from DateTime import DateTime
from Products.ATContentTypes.utils import DT2dt
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin
from Products.ATContentTypes.interfaces import ICalendarSupport

# gcommons
from gcommons.Core.lib.relators import RelatorsMixin
from journalcommons.Conference import ConferenceMessageFactory as _
from journalcommons.Conference.interfaces import IConferenceEvent
from journalcommons.Conference.config import PROJECTNAME



ConferenceEventSchema = folder.ATFolderSchema.copy() + RelatorsMixin.schema.copy() + atapi.Schema((
    atapi.StringField(
        name='eventType',
        required=True,
        searchable=1,
        storage=atapi.AnnotationStorage(),
        vocabulary='listConferenceEventTypes',
        enforceVocabulary=True,
        widget = SelectDescriptionWidget(            
            label="Type",            
            description="Choose the type of event that best fits what you are proposing",
            #label_msgid="jcommons_event_title",            
            #description_msgid="jcommons_help_draft_title",            
        ),
    ),

    atapi.TextField('text',              
        required=False,              
        searchable=True,              
        primary=True,              
        storage = atapi.AnnotationStorage(),
        validators = ('isTidyHtmlWithCleanup',),              
        default_output_type = 'text/x-html-safe',              
        widget = atapi.RichWidget(                        
                    description = 'Describe thoroughly your proposal',                        
                    label = _(u'label_description', default=u'Description'),                        
                    rows = 25,
                    allow_file_upload = True,                        
        ),    
    ),
    atapi.ComputedField('description',        
        searchable=1,        
        expression='context._compute_description()',       
    ),
                                                                     

    #TODO: Move all this fields somewhere to common event schema
    # with boilerplate code and reasonable defaults
    # e.g. this can all be Conference values if no better value.
    atapi.StringField(
        name='venue',
        required=False,
        searchable=1,
#        write_permission = ChangeConferenceSchedule,                  
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            visible = {'edit' : 'invisible', 'view' : 'invisible' },
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
#        write_permission = ChangeConferenceSchedule,                  
        default_method=DateTime,                  
        languageIndependent=True,                  
        widget = atapi.CalendarWidget(                        
            visible = {'edit' : 'invisible', 'view' : 'invisible' },
            description = '',                        
            label = _(u'label_event_start', 
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
            visible = {'edit' : 'invisible', 'view' : 'invisible' },
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
#                write_permission = ChangeEvents,               
                visible = {'edit' : 'invisible', 'view' : 'invisible' },
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
                visible = {'edit' : 'invisible', 'view' : 'invisible' },
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
                visible = {'edit' : 'invisible', 'view' : 'invisible' },
                validators= (),                
                widget = atapi.StringWidget(                        
                                      description = '',                        
                                      label = _(u'label_contact_phone', 
                                                default=u'Contact Phone')                        
                )),
))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

def finalizeConferenceEventSchema(schema):
    schema['title'].storage = atapi.AnnotationStorage()
    schema['description'].storage = atapi.AnnotationStorage()

    # Call ATContentTypes
    schemata.finalizeATCTSchema(
        schema,
        folderish=True,
        moveDiscussion=False
    )
    return schema



class ConferenceEvent(folder.ATFolder, RelatorsMixin):
    """An event within a Conference"""
    implements(IConferenceEvent)

    meta_type = "ConferenceEvent"
    schema = finalizeConferenceEventSchema(ConferenceEventSchema)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    eventType = atapi.ATFieldProperty('eventType')
    
    
    def listConferenceEventTypes(self, extended=False):
        context = aq_inner(self)
        config = context.aq_getConfig()
        
        type = config.getItemType_byPortalType('ConferenceEvent')
            
        if not extended:
            return atapi.DisplayList([(subtype.id(),subtype.name()) for subtype in  type.subtypes() ])
        else:
            dic = {}
            for subtype in  type.subtypes():
                text = "<b>Description:</b> %s" % subtype.description()
                if subtype.requirements():
                    text = text + "<br/><b>Requirements:</b> %s" % subtype.requirements()
                dic[subtype.id()] = text
            return dic 


    def _compute_description(self):
        return "A %s on '%s'" % (self.eventType, self.title)
    
    """ Helpers to share interface with Events
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
    
    def event_url(self):
        return self.absolute_url()

    ###COMMON! (this is 'Submittable item)
    def get_item_subtype(self, name=False):
        """
        name: return enduser string if true, else
        returns id
        """
        if name:
            vocab = self.listConferenceEventTypes()
            return vocab.getValue( self.getEventType() )
        else:
            return self.getEventType()
    
    def get_review_state(self):
        review_state = self.portal_workflow.getInfoFor(self, 'review_state');
        return review_state
    
    def get_state_comments(self):
        review_state = self.get_review_state()
        if review_state == 'draft':
            return "Your need to finish editing your paper and submit it to editors for evaluation"
        elif review_state == 'eb_draft':
            return "Your paper is awaiting evaluation by editors"
        else:
            return review_state

    
atapi.registerType(ConferenceEvent, PROJECTNAME)

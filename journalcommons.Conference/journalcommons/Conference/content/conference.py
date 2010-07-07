"""Definition of the Conference content type
"""

import logging
from zope.interface import implements, directlyProvides
from Acquisition import aq_inner
from AccessControl import ClassSecurityInfo

from Products.CMFCore.permissions import ModifyPortalContent, View
from Products.CMFCore.utils import getToolByName
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


logger = logging.getLogger('jcommons.Conference.content.Conference')


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
    venue = atapi.ATFieldProperty('venue')

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



    """
    Items to share with jcommons
    """
    def aq_getSubmissionsConfig(self):
        return Conference.config_Submissions
    
    def aq_getContainerName(self):
        logger.warning("DEPRECATED! aq_getContainerName")
        return "Conference"
    def aq_getItemsName(self):
        logger.warning("DEPRECATED! aq_getItemsName")
        return "Conference Paper"
    def aq_getItemsType(self):
        logger.warning("DEPRECATED! aq_getItemsType")
        return "ConferencePaper"
    def aq_stateDraftsAllowed(self):
        logger.warning("DEPRECATED! aq_stateDraftsAllowed")
        return False
    
    def at_post_create_script(self):
        """ Create a folder for Submissions
        """
        fldid = self.invokeFactory('SubmissionsFolder', 'submit', title = 'Submissions',
                        description='This folder holds paper submissions')

    # TODO!!! remove this
    # TODO: configurable stuff!
    config_Submissions = {
            'ContainerName':'Conference',
            'Items': [ { 'name': 'Conference Paper',
                         'type': 'ConferencePaper',
                         'description': """Successful papers will reach several constituencies of the organization and will connect analysis to social, political, economic, or ethical questions.

                                        Proposals for papers should include: the title of the paper; the name, title, affiliation, and email address for the author; and an abstract of the 20 minute paper (<500 words).
                                        """,
                         },
                       { 'name': 'Conference Session',
                         'type': 'ConferenceEvent',
                         'description': """ There are different types of this sessions:
                         """,
                         'subtypes': [ {
                                  'id': 'panel',
                                  'name': 'Pre-Constituted Panel',
                                  'description':  "Pre-constituted panels allow a team of 3-4 individuals may present their research, work, and/or experiences, leaving 30-45 minutes of the session for questions and discussion.  Panels should include 3-4 participants.",
                                  'requirements': """                  
                                  the title of the panel; 
                                    the name, title, affiliation, and contact information of the panel organizer; 
                                    the names, titles, affiliations, and email addresses of all panelists, 
                                    and a chair and/or discussant; 
                                a description of the panels topic (<500 words); 
                                and abstracts for each presentation (<150 words).
                                """,
                                },
                                {
                                  'id': 'roundtable',
                                 'name': 'Roundtable',
                                 'description': "Roundtables allow a group of participants to convene with the goal of generating discussion around a shared concern.  In contrast to panels, roundtables typically involve shorter position or dialogue statements (5-10 minutes) in response to questions distributed in advance by the organizer.  The majority of roundtable sessions should be devoted to discussion.  Roundtables are limited to no more than five participants, including the organizer.  We encourage roundtables involving participants from different institutions, centers, and organizations.", 
                                 'requirements': """
                                    Proposals for roundtables should include: 
                                        the title of the roundtable; 
                                        the name, title, affiliation, and contact information of the roundtable organizer; 
                                        the names, titles, affiliations, and email addresses of the proposed roundtable participants; 
                                        and a 
                                        description of the position statements, questions, or debates that will be under discussion (<500 words).
                                    """, 
                                },
                                {
                                  'id': 'workshop',
                                 'name': 'Workshop',
                                 'description': "Workshops allow a facilitator or facilitating team to set an agenda, pose opening questions, and/or organize hands-on participant activities.  The facilitator or team is responsible for gathering responses and results from participants and helping everyone digest them.", 
                                 'requirements': """
                                    Proposals for workshops should include: 
                                    the title of the workshop; the name, title, affiliation, and contact information of the (lead) facilitator and for any co-facilitators; 
                                    a description of the activities to be undertaken (<500 words).  
                                    Please also include a description of space requirements, if appropriate
                                    """,
                                },
                                {
                                  'id': 'seminar',
                                 'name':'Seminar',
                                 'description': """Seminars are small-group (maximum 15 individuals) discussion sessions for which participants prepare in advance of the conference.  In previous years, preparation has involved shared readings, pre-circulated ''position papers'' by seminar leaders and/or participants, and other forms of pre-conference collaboration.  We particularly invite proposals for seminars designed to advance emerging lines of inquiry and research/teaching initiatives within cultural studies broadly construed.  We also invite seminars designed to generate future collaborations among conference attendees.  Once a limited number of seminar topics and leaders are chosen, the seminars will be announced through the CSA's various public e-mail lists. Participants will contact the seminar leader(s) directly who will then inform the Program Committee who will participate in the seminar.  Seminars will be marked in the conference programs as either closed to non-participants or open to other conference attendees as auditors (or in other roles).  
        
                                    A limited number of seminars will be selected by the program committee, with a call for participation announced on the CSA webpage and listserv no later than 4 October 2010.  Interested parties will apply directly to the seminar leader(s) for admission to the session by 12 November 2010.  Seminar leader(s) will be responsible for providing the program committee with a confirmed list of participants (names, titles, affiliations, and email addresses required) for inclusion in the conference program no later than 22 November 2010.  Please note: To run at the conference, seminars must garner a minimum of 8 participants, in addition to the seminar leader(s).
                                    Individuals interested in participating in (rather than leading) a seminar should consult the list of seminars and the instructions for signing up for them, available at conference website after 4 October 2010.  Please direct questions about seminars to S. Charusheela: s.charsheela@unlv.edu.
                                    """, 
                                'requirements': """
                                    Proposals for seminars should include: 
                                    the title of the seminar; the name, title, affiliation, and contact information of the seminar leader/team members; 
                                    and a description of the issues and questions that will be raised in discussion, along with a description of the work to be completed by participants in advance of the seminar (<500 words).  Examples of successful seminar descriptions are available on the conference website.
                                    """
                                },
                                {
                                  'id': 'divsession',
                                 'name':'Division Session',
                                 'description':"A list of CSA divisions is available at http://www.csaus.pitt.edu.  All divisions have two sessions at their command.  Divisions may elect to post calls on the CSA site for papers and procedures for submission to division sessions or handle the creation of their two division sessions by other means.  Division chairs will submit their two sessions, including the appropriate information as listed above, to the conference website.  They should also email their two sessions directly to the CSA’s “division wrangler” – Sora Han: sora.han@uci.edu – by 17 September 2010.",                         
                        }
        ]
    }
    ],
    }


atapi.registerType(Conference, PROJECTNAME)

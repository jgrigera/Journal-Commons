"""Definition of the Conference content type
"""

from zope.interface import implements, directlyProvides

import zipfile
from cStringIO import StringIO

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ModifyPortalContent, View
from Products.CMFCore.utils import getToolByName


# Archetypes
from Products.Archetypes import atapi
from plone.app.folder import folder
from Products.ATContentTypes.content import schemata
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

from Products.DataGridField.DataGridWidget import DataGridWidget
from Products.DataGridField.DataGridField import DataGridField
from Products.DataGridField.Column import Column

# Journal Commons
from gcommons.Core.permissions import Vote as permission_Vote
from gcommons.Core.permissions import EditorsMeetingChangeDate as permission_EditorsMeetingChangeDate
from gcommons.Journal import JournalMessageFactory as _
from gcommons.Journal.interfaces import IEditorsMeeting
from gcommons.Journal.config import PROJECTNAME

# Event support
from DateTime import DateTime
from Products.ATContentTypes.utils import DT2dt
from Products.ATContentTypes.lib.calendarsupport import CalendarSupportMixin
from Products.ATContentTypes.interfaces import ICalendarSupport

# Voting
from zope.component import getUtility
from gcommons.Core.interfaces.utilities import IVoteStorage



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
        write_permission = permission_EditorsMeetingChangeDate,
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

    DataGridField(
        name='pollOptionsInput',
        write_permission = permission_EditorsMeetingChangeDate,
        widget=DataGridWidget(
            label=_("Poll Options"),
            description = _('List here the available options for the date poll.'),
            columns={
                'date': Column(_(u'Date')),
                'time': Column(_(u'Time')),
                'comment': Column(_('Comment')),
            },
        ),
        allow_empty_rows=False,
        required=False,
        columns=('date', 'time', 'comment')
    ),

    atapi.LinesField(
        name='agenda',
        widget = atapi.LinesWidget(
            label="Agenda topics",
            description="Add here proposed topics for the meeting.",
            i18n_domain='gcommons.Journal',
        ),
        searchable=True,
    ),


    atapi.ReferenceField('readingList',
        relationship = 'reading',
        multiValued = True,
        keepReferencesOnCopy = True,
        widget = ReferenceBrowserWidget(
            allow_search = True,
            allow_browse = True,
            show_indexes = False,
            force_close_on_insert = False,
            #only_for_review_states = 'eb_draft',
            base_query={'portal_type': ('Article',),        # TODO: restrict this type to journal/conf
                        'review_state':('eb_draft',)},      
            label = _(u'label_reading_list', default=u'Reading List'),
            description = "Please select all the items that will be discussed in this meeting",
            visible = {'edit' : 'visible', 'view' : 'invisible' }
        )
    ),

))

                                                
                                                 
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
    security.declareProtected(View, 'download_all_as_zip')
    def download_all_as_zip(self, **kwargs):
        """
        """
        portal_workflow = getToolByName(self, 'portal_workflow')
        data = StringIO()
        out = zipfile.ZipFile(data, 'w')

        for article in self.getReadingList():
            # Write latest draft
            path = '%s.doc' %  article.pretty_title_or_id()
            latestdraft = article.get_current_draft()
            if latestdraft is not None:
                out.writestr(path, latestdraft.get_data())
        
            # Write metadata
            metadata_path = "%s.metadata.txt" % article.pretty_title_or_id()
            #TODO this could be html, coming from a PT...
            metadata_contents = """METADATA FOR ARTICLE

Title: %s

Abstract: 
%s

Keywords: %s

Review History:
%s

No. of Drafts: %s
Latest draft title:  
Word Count: 
URL: %s
""" %       (article.Title(), 
               article.Description(), 
               ';'.join(article.Subject()),  
               portal_workflow.getInfoFor(article,'review_history'),
               article.get_no_drafts(),
               #latestdraft.Title(),
               #latestdraft.getWordCount(),
               article.absolute_url() )            
            out.writestr(metadata_path, metadata_contents)

        out.close()
        data.seek(0)
        return data
        
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
        return 0 #self.end_date - self.start_date
    
    """ Helpers to share interface with Events (and thus use vcs_view, ics_view et.al.)
    """
    def getEventType(self):
        return ("Editors Meeting",)
    
    def event_url(self):
        return self.absolute_url()

    def contact_name(self):
        return None
    def contact_phone(self):
        return None
    def contact_email(self):
        return None

    """ Votes for poll
    """
    def getPollOptions(self):
        if self.pollOptions is None:
            self.pollOptions = {}
        return self.pollOptions
        
    def setPollOptionsInput(self, data):
        field = self.getField('pollOptionsInput')
        field.set(self, data)
        data = field.get(self) # After cleanup by DataGridField

        self.pollOptions = {}
        rid = 0
        for row in data:
            self.pollOptions[rid] = row
            rid += 1
    
    @property
    def vote_storage(self):
        return getUtility(IVoteStorage)
        
    def vote_uid(self):
        return '/'.join(self.getPhysicalPath())
        
    def voter_uid(self):
        portal_membership = getToolByName(self,'portal_membership')
        return portal_membership.getAuthenticatedMember().getId()

    def hasVoted(self):
        return self.vote_storage.has_voted(self.vote_uid(),self.voter_uid())
        
    def getVote(self):
        return self.vote_storage.get_vote(self.vote_uid(),self.voter_uid())
    
    def storeVote(self, vote):
        self.vote_storage.vote(self.vote_uid(),self.voter_uid(),vote)
        
    def getTotalVotes(self, optionId):
        votes = self.vote_storage.get_votes(self.vote_uid())
        count = 0
        if votes is not None:
           for who in votes:
               if optionId in votes[who]:
                   count += 1 
        return count
        
    def getTotalVoters(self):
        votes = self.vote_storage.get_votes(self.vote_uid())
        return len(votes)
    



atapi.registerType(EditorsMeeting, PROJECTNAME)

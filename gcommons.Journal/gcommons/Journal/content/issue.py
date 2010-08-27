"""Definition of the Issue content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from gcommons.Journal import JournalMessageFactory as _
from gcommons.Journal.interfaces import IIssue
from gcommons.Journal.config import PROJECTNAME

IssueSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.ComputedField(
        'title',
        searchable=1,
        expression='context._compute_title()',
        accessor='Title'
    ),

    atapi.StringField(
        name='volume',
        required=False,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        schemata ='default',
        widget=atapi.StringWidget(
            label=_(u"Volume"),
            description=_(u"Volume number in the series"),
        ),
    ),

    atapi.StringField(
        name='number',
        required=False,
        searchable=1,
        storage=atapi.AnnotationStorage(),
        #default='',
        schemata ='default',
        widget=atapi.StringWidget(
            label=_(u"Number"),
            description=_(u"Issue Number"),
        ),
    ),

    atapi.StringField(
        name='date',
        required=True,
        searchable=1,
        storage=atapi.AnnotationStorage(),
        #default='',
        schemata ='default',
        widget=atapi.StringWidget(
            label=_(u"Date"),
            description=_(u"Date associated with the issue"),
        ),
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

IssueSchema['title'].storage = atapi.AnnotationStorage()
IssueSchema['description'].storage = atapi.AnnotationStorage()
IssueSchema['description'].widget.description = 'Optional description (e.g. special issue, guest editors)'
IssueSchema.moveField('description', after='date')



schemata.finalizeATCTSchema(
    IssueSchema,
    folderish=True,
    moveDiscussion=False
)


class Issue(folder.ATFolder):
    """An issue of a journal"""
    implements(IIssue)

    meta_type = "Issue"
    schema = IssueSchema

#    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    volume = atapi.ATFieldProperty('volume')
    number = atapi.ATFieldProperty('number')
    date   = atapi.ATFieldProperty('date')

    def _compute_title(self):
        """Compute title from vol and number"""
        title = []
        # TODO: let user configure this
        if (self.volume is not None) and len(self.volume) > 0:
    	    title.append("Volume %s" % self.volume)
    	if (self.number is not None) and len(self.number) > 0:
    	    title.append("Number %s" % self.number)
    	title.append("%s" % self.date)
    	
        return ', '.join(title)


atapi.registerType(Issue, PROJECTNAME)

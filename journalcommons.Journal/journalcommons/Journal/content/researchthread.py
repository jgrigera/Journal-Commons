"""Definition of the ResearchThread content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from journalcommons.Journal import JournalMessageFactory as _
from journalcommons.Journal.interfaces import IResearchThread
from journalcommons.Journal.config import PROJECTNAME

ResearchThreadSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.ComputedField(
        'id',
        searchable=1,
        expression='context._compute_id()',
        accessor='Id'
    ),

    atapi.StringField(
        name='title',
        required=True,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        schemata ='default',
        widget=atapi.StringWidget(
            label=_(u"Title"),
            description=_(u"Topic/Title of the Research Thread"),
        ),
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
            label=_(u"Volume number"),
            description=_(u"Journal Volume number"),
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
            label=_(u"Number in volume"),
            description=_(u"Issue number in the Volume"),
        ),
    ),

    atapi.StringField(
        name='ends',
        required=True,
        searchable=1,
        storage=atapi.AnnotationStorage(),
        #default='',
        schemata ='default',
        widget=atapi.StringWidget(
            label=_(u"Ends"),
            description=_(u"Date research thread ends"),
        ),
    ),

    atapi.StringField(
        name='frequency',
        required=True,
        searchable=1,
        storage=atapi.AnnotationStorage(),
        default='continuous',
        schemata ='default',
        widget=atapi.StringWidget(
            label=_(u"Frequency"),
            description=_(u"Frequency of publication: continuous or number in months"),
        ),
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

ResearchThreadSchema['title'].storage = atapi.AnnotationStorage()
ResearchThreadSchema['id'].storage = atapi.AnnotationStorage()
ResearchThreadSchema['description'].storage = atapi.AnnotationStorage()
ResearchThreadSchema['description'].widget.description = 'Optional description (e.g. special issue, guest editors)'
ResearchThreadSchema.moveField('description', after='ends')

schemata.finalizeATCTSchema(
    ResearchThreadSchema,
    folderish=True,
    moveDiscussion=False
)

class ResearchThread(folder.ATFolder):
    """ResearchThread, an issue that is open to submissions for a long period of time"""
    implements(IResearchThread)

    meta_type = "ResearchThread"
    schema = ResearchThreadSchema
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    title = atapi.ATFieldProperty('id')
    subject = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    volume = atapi.ATFieldProperty('volume')
    number = atapi.ATFieldProperty('number')
    ends   = atapi.ATFieldProperty('ends')
    frequency   = atapi.ATFieldProperty('frequency')

    def _compute_id(self):
        """Compute title from vol and number"""
        title = []
        # TODO: let user configure this
        if (self.volume is not None) and len(self.volume) > 0:
    	    title.append("vol %s" % self.volume)
    	if (self.number is not None) and len(self.number) > 0:
    	    title.append("no %s" % self.number)
        title.append(" ENDS %s" % self.ends)
    	
        return ', '.join(title)

atapi.registerType(ResearchThread, PROJECTNAME)

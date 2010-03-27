"""Definition of the ConferencePaper content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from journalcommons.Conference import ConferenceMessageFactory as _
from journalcommons.Conference.interfaces import IConferencePaper
from journalcommons.Conference.config import PROJECTNAME


ConferencePaperSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        name='specialRequirements',
        required=False,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Special Requirements"),
            description=_(u"Does your paper require any specific requirements? Type any special requirements here (such as Powerpoint, video equipment, etc)"),
        ),
    ),
))


# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.
def finalizeConferenceSchema(schema):
    schema['title'].storage = atapi.AnnotationStorage()
    schema['description'].storage = atapi.AnnotationStorage()
    schema['description'].required = True
    schema['description'].widget.label = _('Abstract')
    schema['description'].widget.description = _('A short summary of your article.')
    schema['creators'].storage = atapi.AnnotationStorage()
    schema['creators'].searchable = True
    schema['creators'].widget.label = _('Authors')
    schema['creators'].widget.description = _('Authors of the paper or persons responsible for this piece. Please enter a list of names, one per line. The principal creator should come first.')
    schema['subject'].storage = atapi.AnnotationStorage()
    schema['subject'].widget.label = _('Keywords')
    schema['subject'].widget.description  = _('Please select among the existing keywords or add new ones to describe the subjects of your submission.')

    
    # Hide this fields
    for field in ('effectiveDate', 'expirationDate',):
        schema[field].widget.visible = {'edit': 'invisible', 'view': 'invisible'}
    
    # Call ATContentTypes
    schemata.finalizeATCTSchema(
        schema,
        folderish=True,
        moveDiscussion=False
    )
    
    # Fix after ATContentTypes
    # Reorder
    schema.moveField('creators', after='title')
    schema.moveField('description', after='creators')
    schema.moveField('subject', after='description')
    # Schematas
    schema.changeSchemataForField('creators', 'default')
    schema.changeSchemataForField('subject', 'default')
    return schema
    

class ConferencePaper(folder.ATFolder):
    """A paper submitted to a conference"""
    implements(IConferencePaper)

    meta_type = "ConferencePaper"
    schema = finalizeConferenceSchema(ConferencePaperSchema)
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    specialRequirements = atapi.ATFieldProperty('specialRequirements')
    
    ###COMMON!
    def get_review_state(self):
        review_state = self.portal_workflow.getInfoFor(self, 'review_state');
        return review_state
    
    def get_state_comments(self):
        return "Your article is about to xxx"
    
    def get_drafts(self):
        brains = self.listFolderContents(contentFilter={"portal_type" : "File"})
        #brains = self.portal_catalog({'portal_type':'File',
        #                     'path':'/'.join(self.context.getPhysicalPath()),
        #                     'sort_on':'sortable_title'})
        #groups = [i.getObject() for i in brains]
        return brains
        
    def get_no_drafts(self):
        return len( self.get_drafts() )

atapi.registerType(ConferencePaper, PROJECTNAME)

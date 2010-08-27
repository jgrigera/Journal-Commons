"""Definition of the Draft content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.file import ATFile

from gcommons.Journal import JournalMessageFactory as _
from gcommons.Journal.interfaces import IDraft
from gcommons.Journal.config import PROJECTNAME
import logging
logger = logging.getLogger('gcommons.Journal.content.draft')


DraftSchema = ATFile.schema.copy() + atapi.Schema((

    atapi.StringField(        
        name='title',        
        widget = atapi.SelectionWidget(            
            label="Type",            
            description="Choose the description that best fits the type of draft you are uploading",
            label_msgid="gcommons_draft_title",            
            description_msgid="gcommons_help_draft_title",            
        ),
        required=True,        
        accessor="Title",
        vocabulary="getDraftTypesVocabulary",        
        searchable=True   
    ),
                                                  
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

DraftSchema['title'].storage = atapi.AnnotationStorage()
DraftSchema['description'].storage = atapi.AnnotationStorage()
DraftSchema['description'].widget.description = "Additional notes about this draft"

schemata.finalizeATCTSchema(DraftSchema, moveDiscussion=False)


class Draft(ATFile):
    """File containing a draft of item"""
    implements(IDraft)

    meta_type = "Draft"
    schema = DraftSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
#    security.declareProtected(permissions.View, 'getReleasesVocab')        
    def getDraftTypesVocabulary(self):
        """        
        Get the vocabulary of available draft types
        """        
        vocab = atapi.DisplayList()        
        vocab.add('draft_1', 'First Draft', 'draft_1')        
        vocab.add('draft_2', 'Second Draft', 'draft_2')        
        vocab.add('draft_3', 'Third Draft', 'draft_3')        
        vocab.add('draft_4', 'Later Draft', 'draft_4')        
        vocab.add('draft_f', 'Final Draft', 'draft_f')        
        vocab.add('published', 'Published Version', 'published')        
        return vocab

    def getWordCount(self):
        """
        Return word count of this file
        """
        text = self.SearchableText()
        return len(text.split(None))


atapi.registerType(Draft, PROJECTNAME)

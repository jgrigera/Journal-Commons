"""Definition of the Draft content type
"""
import logging
from zope.interface import implements, directlyProvides
from plone.memoize.instance import memoize

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.file import ATFile

from gcommons.Journal import JournalMessageFactory as _
from gcommons.Journal.interfaces import IDraft
from gcommons.Journal.config import PROJECTNAME

logger = logging.getLogger('gcommons.Journal.content.draft')


#
# Schema
#
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
        
    """
    Prevent this object from being indexed
    """
    def at_post_create_script(self):
        # set_draft is aquired from Article
        logger.info("post Create: set_curr_draft")
        self.set_current_draft(self.id)
        
    def at_post_edit_script(self):
        # set_draft is aquired from Article
        logger.info("post edit: set_curr_draft")
        self.set_current_draft(self.id)
                       
    def indexObject(self):
        logger.info("Boycott of indexObject")
        pass                                                                                                   
    def reindexObject(self,*args,**kwargs):
        logger.info("Boycott of reindexObject")
        pass                                                                                                   

#    security.declareProtected(permissions.View, 'getReleasesVocab')        
    def getDraftTypesVocabulary(self):
        """        
        Get the vocabulary of available draft types
        """        
        vocab = atapi.DisplayList()        
        vocab.add('draft', 'Draft', 'draft')        
        vocab.add('copyedited', 'Copy Edited Version', 'copyedited')        
        vocab.add('published', 'Published Version', 'published')        
        return vocab

    @memoize
    def getWordCount(self):
        """
        Return word count of this file
        """
        logger.info("Calculating wordcount...")
        text = self.SearchableText()
        wordcount = len(text.split(None))
        return wordcount
    
        
atapi.registerType(Draft, PROJECTNAME)

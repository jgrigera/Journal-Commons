"""Definition of the Draft content type
"""
import os
import logging
from DateTime import DateTime

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent
from zope.interface import implements, directlyProvides
from plone.memoize.instance import memoize

from Products.Archetypes import atapi
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.file import ATFile

from gcommons.Core import CoreMessageFactory as _
from gcommons.Core.interfaces import IDraft
from gcommons.Core.config import PROJECTNAME
import gcommons.Core.permissions as permissions

logger = logging.getLogger('gcommons.Core.content.draft')


#
# Schema
#
DraftSchema = ATFile.schema.copy() + atapi.Schema((
    atapi.ComputedField('title',
        searchable=False,
        expression='context._compute_title()',
        accessor='Title'
    ),

    atapi.StringField(        
        name='subtype',        
        widget = atapi.SelectionWidget(            
            label=_("Type"),            
            description="Choose the description that best fits the type of draft you are uploading",
            label_msgid="gcommons_draft_subtype",            
            description_msgid="gcommons_help_draft_subtype",            
        ),
        required=True,
        storage = atapi.AnnotationStorage(),
        vocabulary="getDraftTypesVocabulary",        
        searchable=False   
    ),
                                                  
))

def finalizeDraftSchema(schema):
    schema['title'].storage = atapi.AnnotationStorage()
    schema['description'].storage = atapi.AnnotationStorage()
    schema['description'].widget.label = "Comments"
    schema['description'].widget.description = "Additional notes about this specific draft, such as known problems or issues fixed"
    schemata.finalizeATCTSchema(schema, moveDiscussion=False)
    return schema



class Draft(ATFile):
    """File containing a draft of item"""
    implements(IDraft)
    meta_type = "Draft"
    schema = finalizeDraftSchema(DraftSchema)
    security = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    subtype = atapi.ATFieldProperty('subtype')
    description = atapi.ATFieldProperty('description')
    
    """
    Computed Attributes
    """    
    def _compute_title(self):
        parent = aq_parent(aq_inner(self))   
        return parent.Title()

    """
    Vocabularies
    """
    security.declareProtected(permissions.View, 'getDraftTypesVocabulary')        
    def getDraftTypesVocabulary(self):
        """        
        Get the vocabulary of available draft types
        """        
        vocab = atapi.DisplayList()        
        vocab.add('draft', 'Draft', 'draft')        
        vocab.add('copyedited', 'Copy Edited Version', 'copyedited')        
        vocab.add('published', 'Published Version', 'published')        
        return vocab

    """
    postChange: change Id and notify parent
    """
    def at_post_create_script(self):
        self.postChange()
    def at_post_edit_script(self):
        self.postChange()

    def postChange(self):
        """
        Change id and filename, fixing extension if necessary
        """
        logger.info("postChange: newId and notifyParent")
        if self.subtype is not None:
            now = DateTime()
            self.setId("%s-%s" % (self.subtype,now.strftime('%Y-%m-%d-%H-%M')))
            # Deal with filename
            filefield = self.getField('file')
            filename = filefield.getFilename(self)
            basename, extension = os.path.splitext(filename)

            # Guess a correct extension according to MimeType
            mimetypes_registry = getToolByName(self, 'mimetypes_registry', None)
            mtype = mimetypes_registry.lookup(filefield.getContentType(self))
            try:
                suggestedext = mtype[0].extensions[0]        
            except:
                pass
            logger.info("suggesting %s" % suggestedext)
            
            if len(extension) <= 0:
                extension = ".%s" % suggestedext
            logger.info("Filename is %s, extension %s" % (filename, extension))

            filefield.setFilename(self, "%s-%s%s" % (self.subtype,now.strftime("%Y%m%d"),extension))
        
        parent = aq_parent(aq_inner(self))   
        parent.set_current_draft(self.id)
        parent.reindexObject()
                       
    """
    Prevent this object from being indexed
    """
    def indexObject(self):
        logger.info("Draft Boycott of indexObject")
        pass                                                                                                   
    def reindexObject(self,*args,**kwargs):
        logger.info("Draft Boycott of reindexObject")
        pass                                                                                                   

        
    @memoize
    def getWordCount(self):
        """
        Return word count of this file
        """
        logger.info("Calculating wordcount...")
        text = self.SearchableText()
        wordcount = len(text.split(None))
        return wordcount
    
    @memoize
    def getPageEstimate(self):
        """
        Return estimated number of pages
        """
        parent = aq_parent(aq_inner(self))   
        config = parent.get_item_subtype_config()
        wordcount = self.getWordCount()
        wpp = config.words_per_page()
        if wpp > 0:
            return wordcount / wpp 
        else:
            return 0 
    
    security.declareProtected(permissions.View, 'preview_as_html')
    def preview_as_html(self):
        """
        public
        """
        portal_transforms = getToolByName(self, 'portal_transforms')
        filefield = self.getField('file')
        datastream = ''
        try:
            datastream = portal_transforms.convertTo("text/html", 
                                                     str(filefield.get(self, raw=True)), 
                                                     mimetype = filefield.getContentType(self), 
                                                     filename = filefield.getFilename(self))
        except Exception, e:
            logger.info("Error while trying to convert file contents to 'text/html': %s" % e)
        return str(datastream)
        
        
    def getAlternativeFormats(self):
        """ 
        Return a list of possible formats we can
        output the draft to
        """
        return
        #TODO: not finished!
        portal_transforms = getToolByName(self, 'portal_transforms')
        filefield = self.getField('file')
        startingType = filefield.getContentType(self) 
        logger.info("startingType %s" % startingType)

        outputs = portal_transforms._mtmap.get(startingType)                                                                                                                                         
        if outputs:                                                                                                                                                                     
            for reachedType, transforms in outputs.items():  
                logger.info("%s %s " %(reachedType, transforms))
        
atapi.registerType(Draft, PROJECTNAME)

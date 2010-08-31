"""Definition of the Article content type
"""

from Acquisition import aq_base, aq_inner
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from gcommons.Core.widgets.SelectDescriptionWidget import SelectDescriptionWidget

from gcommons.Core.lib.relators import RelatorsMixin
from gcommons.Journal import JournalMessageFactory as _
from gcommons.Journal.interfaces import IArticle
from gcommons.Journal.config import PROJECTNAME


import logging
logger = logging.getLogger('gcommons.Journal.content.article')


#
# Schema
#
ArticleSchema = folder.ATFolderSchema.copy() + RelatorsMixin.schema.copy() + atapi.Schema((
    atapi.StringField(
        name='articleType',
        required=True,
        searchable=1,
        storage=atapi.AnnotationStorage(),
        vocabulary='listArticleTypes',
        enforceVocabulary=True,
        widget = SelectDescriptionWidget(            
            label="Type",            
            description="Choose the type of article that best fits your piece",
            label_msgid="gcommons_article_type",            
            description_msgid="gcommons_help_article_type",            
        ),
    ),

    # -*- Your Archetypes field definitions here ... -*-
    atapi.ComputedField(
        'bibreference',
        searchable=1,
        expression='context._compute_bibreference()',
        accessor='BibReference'
    ),

    atapi.StringField(
        name='pages',
        required=False,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        schemata ='bibdata',
        widget=atapi.StringWidget(
            label=_(u"Pages"),
            description=_(u"Page range of published article"),
        ),
    ),

    atapi.StringField(
        name='doi',
        required=False,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        schemata ='bibdata',
        widget=atapi.StringWidget(
            label=_(u"DOI"),
            description=_(u"Digital Object Identifier for this article"),
        ),
    ),

    atapi.StringField(
        name='extraData',
        required=False,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        schemata ='bibdata',
        widget=atapi.StringWidget(
            label=_(u"Extra Data"),
            description=_(u"Any comments, piece type, further info"),
        ),
    ),

    atapi.StringField(
        name='manager',
        required=False,
        searchable=False,
        write_permission='Manage Portal',
        #default='',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Responsible Manager"),
            description=_(u"Editor in charge of dealing with this article"),
            visible = {'edit': 'invisible', 'view': 'invisible'},
        ),
    ),

))


def finalizeArticleSchema(schema):
    schema['title'].storage = atapi.AnnotationStorage()
    schema['title'].widget.description = _(u"Article title.")
    schema['description'].storage = atapi.AnnotationStorage()
    schema['description'].required = True
    schema['description'].widget.label = _('Abstract')
    schema['description'].widget.description = _('A short summary of your article.')
    schema['subject'].storage = atapi.AnnotationStorage()
    schema['subject'].widget.label = _('Keywords')
    schema['subject'].widget.description  = _('Please select among the existing keywords or add new ones to describe the subjects of your article.')
 
    # Reorder
    schema.moveField('description', after=RelatorsMixin.lastField)
    schema.moveField('subject', after='description')
    
    # Hide this fields
    for field in ('effectiveDate', 'expirationDate', 'allowDiscussion'):
        schema[field].widget.visible = {'edit': 'invisible', 'view': 'invisible'}
    
    # Call ATContentTypes
    schemata.finalizeATCTSchema(
        schema,
        folderish=True,
        moveDiscussion=False
    )
    
    # Fix after ATContentTypes
    schema.changeSchemataForField('subject', 'default')
    return schema



class Article(folder.ATFolder, RelatorsMixin):
    """An article in an issue of a journal"""
    implements(IArticle)
    
    meta_type = "Article"
    schema = finalizeArticleSchema(ArticleSchema)

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    articleType = atapi.ATFieldProperty('articleType')
    pages = atapi.ATFieldProperty('pages')
    doi = atapi.ATFieldProperty('doi')


    
    @property
    def portal_workflow(self):
        return getToolByName(self.context, 'portal_workflow')

    """
    Helpers for Schema
    """
    def listArticleTypes(self, extended=False):
        context = aq_inner(self)
        config = context.aq_getConfig()
        
        type = config.getItemType_byPortalType('Article')
            
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


    def _compute_bibreference(self):
        return "TODO: bibreference"

    def get_responsible_manager(self):
        if self.manager is not None:
            return self.manager
        else:
            return "UNASSIGNED"

    # Common...
    def get_container(self):
        logger.info("?? Deprecated article.get_container()?")
        return None

    def get_item_subtype(self, name=False):
        if name:
            vocab = self.listArticleTypes(False)
            return vocab.getValue( self.articleType )
        else:
            return self.articleType

    def get_item_subtype_config(self, name=False):
        context = aq_inner(self)
        config = context.aq_getConfig()
        
        type = config.getItemType_byPortalType('Article')
        return type.getSubtype_byId(self.get_item_subtype(False))

    def get_review_state(self):
        review_state = self.portal_workflow.getInfoFor(self, 'review_state');
        #TODO: move to common!
        return review_state
    
    def get_state_comments(self):
        review_state = self.get_review_state()
        if review_state == 'draft':
            return "Your need to finish editing your paper and submit it to editors for evaluation"
        elif review_state == 'eb_draft':
            return "Your paper is awaiting evaluation by editors"
        else:
            return "Your paper is now %s" % review_state
    
    """
    Draft Management
    """
    def get_current_draft(self):
        try:
            return getattr(self, self.current_draft_id)  
        except AttributeError:
            drafts = self.get_drafts()
            if len(drafts):
                return drafts.pop()
        return None
    
    def set_current_draft(self, idx=None):
        self.current_draft_id = idx

    def get_drafts(self):
        brains = self.listFolderContents(contentFilter={"portal_type" : ('Draft',), 'sort_on': 'created'})#, 'sort_order' : 'reverse'})
        return brains
        
    def get_no_drafts(self):
        return len( self.get_drafts() )
    
    def SearchableText(self):
        """
        We index the content of the draft as own, so that searches
        of fulltext comes to parent object and not individual draft 
        """
        current_draft = self.get_current_draft()
        if current_draft is not None:
            return folder.ATFolder.SearchableText(self) + current_draft.SearchableText()
        else:
            return folder.ATFolder.SearchableText(self)
      

atapi.registerType(Article, PROJECTNAME)

"""Definition of the Article content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName

from journalcommons.Journal import JournalMessageFactory as _
from journalcommons.Journal.interfaces import IArticle
from journalcommons.Journal.config import PROJECTNAME

ArticleSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.ComputedField(        
        'title',        
        searchable=1,        
        expression='context._compute_title()',       
        accessor='Title'    
    ),

    atapi.ComputedField(
        'bibreference',
        searchable=1,
        expression='context._compute_bibreference()',
        accessor='BibReference'
    ),

    atapi.StringField(
        name='article_title',
        required=True,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        schemata ='default',
        widget=atapi.StringWidget(
            label=_(u"Title"),
            description=_(u"Article title."),
        ),
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

))


def finalizeArticleSchema(schema):
    schema['description'].storage = atapi.AnnotationStorage()
    schema['description'].required = True
    schema['description'].widget.label = _('Abstract')
    schema['description'].widget.description = _('A short summary of your article.')
    schema['creators'].storage = atapi.AnnotationStorage()
    schema['creators'].searchable = True
    schema['creators'].widget.label = _('Authors')
    schema['creators'].widget.description = _('Authors of the article or persons responsible for this piece. Please enter a list of names, one per line. The principal creator should come first.')
    schema['subject'].storage = atapi.AnnotationStorage()
    schema['subject'].widget.label = _('Keywords')
    schema['subject'].widget.description  = _('Please select among the existing keywords or add new ones to describe the subjects of your article.')

    # Reorder
    schema.moveField('creators', after='article_title')
    schema.moveField('description', after='creators')
    schema.moveField('subject', after='description')
    
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
    schema.changeSchemataForField('creators', 'default')
    schema.changeSchemataForField('subject', 'default')
    return schema


class Article(folder.ATFolder):
    """An article in an issue of a journal"""
    implements(IArticle)
    
    meta_type = "Article"
    schema = finalizeArticleSchema(ArticleSchema)

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    title = atapi.ATFieldProperty('title')
    article_title = atapi.ATFieldProperty('article_title')
    description = atapi.ATFieldProperty('description')
    pages = atapi.ATFieldProperty('pages')
    doi = atapi.ATFieldProperty('doi')

    @property
    def portal_workflow(self):
        return getToolByName(self.context, 'portal_workflow')

    def _compute_title(self):
        # TODO: something like "pp.." or short title
        #if len (self.article_title) > 10:
        #    return self.article_title[:10]+'...'
        #else:
        return self.article_title
    
    def _compute_bibreference(self):
    	return "TODO: bibreference"
 
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
    
    	
		
atapi.registerType(Article, PROJECTNAME)

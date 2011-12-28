"""Definition of the Article content type
"""

from Acquisition import aq_base, aq_inner
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Archetypes import atapi
from plone.app.folder import folder
from Products.ATContentTypes.content import schemata
from gcommons.Core.widgets.SelectDescriptionWidget import SelectDescriptionWidget
from gcommons.Core.widgets.AjaxKeywordsWidget import AjaxKeywordsWidget

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
        name='actioneditor',
        required=False,
        searchable=False,
        write_permission='Manage Portal',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Action Editor"),
            description=_(u"Editor in charge of dealing with this article"),
            visible = {'edit': 'invisible', 'view': 'invisible'},
        ),
    ),

    atapi.StringField(
        name='teaserHead',
        required=False,
        searchable=0,
        storage=atapi.AnnotationStorage(),
        schemata ='publish',
        widget=atapi.StringWidget(
            label=_(u"Teaser headline"),
            description=_(u"Headline for the teaser appearing with published article"),
        ),
    ),

    atapi.StringField(
        name='teaserBody',
        required=False,
        searchable=0,
        storage=atapi.AnnotationStorage(),
        schemata ='publish',
        widget=atapi.TextAreaWidget(
            label=_(u"Teaser body"),
            description=_(u"Text for the teaser appearing with published article"),
        ),
    ),

    atapi.TextField(
            name='publishedText',
#            allowable_content_types=('text/html'),
#            default_output_type='text/x-html-safe',
            searchable=1,
            storage=atapi.AnnotationStorage(),
            schemata ='publish',
            required=False,
            widget=atapi.RichWidget(
                label=_(u"Published text"),
                description=_(u"Text of the published article"),
            ),
     ),
                                                                                          
    # atapi.StringField(
    #     name='publishedText',
    #     required=False,
    #     searchable=0,
    #     storage=atapi.AnnotationStorage(),
    #     schemata ='publish',
    #     allowable_content_types=('text/plain', 'text/structured', 'text/html','text/x-web-intelligent'),
    #     widget=atapi.TextAreaWidget(
    #         label=_(u"Published text"),
    #         description=_(u"Text of the published article"),
    #     ),
    #     default_content_type="text/x-web-intelligent", 
    #     default_output_type="text/html", 
    # ),

   atapi.ImageField('image',
        required=False,
        storage=atapi.AnnotationStorage(),
        schemata ='publish',
        sizes={'thumb': (80,80),
               'mini': (32,32),
               'normal': (240,140)},
        widget=atapi.ImageWidget(label=_(u"Article Image"),
                                 description=_(u"Used as a cover image when article is published"))
    ),
   atapi.ImageField('image2',
        required=False,
        storage=atapi.AnnotationStorage(),
        schemata ='publish',
        sizes={'thumb': (80,80),
               'mini': (32,32),
               'normal': (240,140)},
        widget=atapi.ImageWidget(label=_(u"Article Image 2"),
                                 description=_(u"Used as a cover image when article is published"))
    ),
   atapi.ImageField('image3',
        required=False,
        storage=atapi.AnnotationStorage(),
        schemata ='publish',
        sizes={'thumb': (80,80),
               'mini': (32,32),
               'normal': (240,140)},
        widget=atapi.ImageWidget(label=_(u"Article Image 3"),
                                 description=_(u"Used as a cover image when article is published"))
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
    #schema['subject'].widget.label = _('Keywords')
    #schema['subject'].widget.description  = _('Please select among the existing keywords or add new ones to describe the subjects of your article.')
    schema['subject'].widget = AjaxKeywordsWidget(
                label=_('Keywords'),
                description=('Please select among the existing keywords or add new ones to describe the subjects of your article. Use semicolon or press ENTER to add a tag.')
    )
 
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



class Article(folder.ATFolder,RelatorsMixin):
    """An article in an issue of a journal"""
    implements(IArticle)
    
    meta_type = "Article"
    schema = finalizeArticleSchema(ArticleSchema)

    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    articleType = atapi.ATFieldProperty('articleType')
    actioneditor = atapi.ATFieldProperty('actioneditor')
    pages = atapi.ATFieldProperty('pages')
    teaserHead = atapi.ATFieldProperty('teaserHead')
    teaserBody = atapi.ATFieldProperty('teaserBody')
#    publishedText = atapi.ATFieldProperty('publishedText')
    publishedText = atapi.ATFieldProperty('publishedText')
    image = atapi.ATFieldProperty('image')
    image2 = atapi.ATFieldProperty('image2')
    image3 = atapi.ATFieldProperty('image3')
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

    def get_action_editor(self, memberObject=False):
        """ 
        Returs current action editor for this article
        if memberObject is true, an object from portal_membership is returned
        otherwise, a string with memberId
        """
        if self.actioneditor is None:
            return None
            
        if memberObject is True:
            portal_membership = getToolByName(self, 'portal_membership')
            member = portal_membership.getMemberById(self.actioneditor)
            return member
        else:
            return self.actioneditor
    
    def set_action_editor(self, editorid):
        self.actioneditor = editorid
        self.reindexObject()

    # Common...
    def get_container(self):
        """ TODO: Find out if we are part of any section/Issue/other container
        """
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
            
    """
    Workflow guards
    """
    def wfguard_canSubmitToEB(self):
        if self.get_no_drafts() > 0:
           return True
        else:
           return False
      

atapi.registerType(Article, PROJECTNAME)

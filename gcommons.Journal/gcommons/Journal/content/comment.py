"""Definition of the Comment content type
"""

from zope.interface import implements, directlyProvides
from Acquisition import aq_inner, aq_parent

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

from gcommons.Journal import JournalMessageFactory as _
from gcommons.Journal.interfaces import IComment
from gcommons.Journal.config import PROJECTNAME

CommentSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.ComputedField('title',
        searchable=1,
        expression='context._compute_title()',
        accessor='Title'
    ),

    atapi.StringField('commentType',
        widget = atapi.SelectionWidget(            
            label="Type",            
            description="Describe correctly the type of comment. Different types will be visible for different users.",
            label_msgid="gcommons_comment_type",            
            description_msgid="gcommons_help_comment_type",            
        ),
        required=True,        
        vocabulary="getCommentTypesVocabulary",        
        searchable=True   
    ),
    
    atapi.ReferenceField('refDraft',
        relationship = 'refDraft',
        multiValued = False,
        default_method = 'getDefaultRefDraft',
        widget = ReferenceBrowserWidget(
            visible = {'edit' : 'invisible', 'view' : 'visible' }
        )
    ),

    atapi.TextField('text',              
        required=False,              
        searchable=True,              
        primary=True,              
        storage = atapi.AnnotationStorage(),
        validators = ('isTidyHtmlWithCleanup',),              
        default_output_type = 'text/x-html-safe',              
        widget = atapi.RichWidget(                        
                    description = '',                        
                    label = _(u'label_body_text', default=u'Body Text'),                        
                    rows = 25,
                    allow_file_upload = True,                        
        ),    
    ),
   

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.
CommentSchema['title'].storage = atapi.AnnotationStorage()
CommentSchema['description'].storage = atapi.AnnotationStorage()
CommentSchema['description'].widget.visible = {'edit' : 'invisible', 'view' : 'invisible' }
schemata.finalizeATCTSchema(CommentSchema, moveDiscussion=False)


class Comment(base.ATCTContent):
    """Object containing comments for an article"""
    implements(IComment)

    meta_type = "Comment"
    schema = CommentSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    
    def _compute_title(self):
        return "%s by %s" % (self.getCommentType(), ','.join(self.listCreators()))
    
    def getDefaultRefDraft(self):
        # Aqcuire this explicitly just for code clarity
        return aq_parent(self).get_current_draft()
        
    def getCommentTypesVocabulary(self):
        """        
        Get the vocabulary of available draft types
        """        
        vocab = atapi.DisplayList()        
        vocab.add('internal', 'Internal EB Comment', 'internal')        
        vocab.add('referee',  'Referee Report', 'referee')        
        vocab.add('report',   'Report for the Author', 'report')        
        # TODO: permission.. assigned. 
        return vocab

atapi.registerType(Comment, PROJECTNAME)

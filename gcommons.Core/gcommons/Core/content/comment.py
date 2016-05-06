"""Definition of the Comment content type
"""

from zope.interface import implements, directlyProvides
from Acquisition import aq_inner, aq_parent
from Products.CMFCore import permissions
from Products.DCWorkflow.utils import modifyRolesForPermission

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

from gcommons.Core import CoreMessageFactory as _
from gcommons.Core.interfaces import IComment
from gcommons.Core.config import PROJECTNAME

import logging
logger = logging.getLogger('gcommons.Core.content.comment')

CommentSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
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


class CommentType:
    def __init__(self, id, description, view_roles):
        self.id = id
        self.description = description
        self.view_roles = view_roles
       
    def getId(self):
        return self.id
        
    def getTuple(self):
        return (self.id, self.description, self.id)

    def getViewRoles(self):
        return self.view_roles


class Comment(base.ATCTContent):
    """Object containing comments for an article"""
    implements(IComment)

    meta_type = "Comment"
    schema = CommentSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    types = (
        CommentType('internal', 'Internal EB Comment', ('EditorialBoard','Owner','Manager',)),
        CommentType('referee',  'Referee Report', ('EditorialBoard','Owner','Manager',)),
        CommentType('report',   'Report for the Author', ('EditorialBoard','JournalAuthor','Owner','Manager',)),
    )

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
        for atype in Comment.types:
            vocab.add(*atype.getTuple())
        return vocab
        
    def setCommentType(self, data):
        field = self.getField('commentType')
        field.set(self, data)
        data = field.get(self) # After cleanup
        
        # Apply permissions according to type
        view_roles = None
        for atype in Comment.types:
            if data == atype.getId():
               view_roles = atype.getViewRoles()
               break
        if view_roles is None:
            return
            
        for view_perm in (permissions.AccessContentsInformation, permissions.View):
            modifyRolesForPermission(self, view_perm, view_roles )# if roles is a tuple, this means not to acquire
        # Only owner can modify this
        modifyRolesForPermission(self,permissions.ModifyPortalContent,('Owner',))

        
        
    

atapi.registerType(Comment, PROJECTNAME)

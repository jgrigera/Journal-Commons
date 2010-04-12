"""Definition of the Comment content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from journalcommons.Journal import JournalMessageFactory as _
from journalcommons.Journal.interfaces import IComment
from journalcommons.Journal.config import PROJECTNAME

CommentSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

CommentSchema['title'].storage = atapi.AnnotationStorage()
CommentSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(CommentSchema, moveDiscussion=False)

class Comment(base.ATCTContent):
    """Object containing comments for an article"""
    implements(IComment)

    meta_type = "Comment"
    schema = CommentSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Comment, PROJECTNAME)

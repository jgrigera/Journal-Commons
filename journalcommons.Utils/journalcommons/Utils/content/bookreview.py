"""Definition of the BookReview content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from journalcommons.Utils import UtilsMessageFactory as _
from journalcommons.Utils.interfaces import IBookReview
from journalcommons.Utils.config import PROJECTNAME

## Book Reviews
# Book Review Container: Folder, MailTemplatesContainer (or journal...)
#BookData
#Link reviewer, article, book data


BookReviewSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    # -*- Your Archetypes field definitions here ... -*-

))


# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.
BookReviewSchema['title'].storage = atapi.AnnotationStorage()
BookReviewSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(BookReviewSchema, moveDiscussion=False)


class BookReview(base.ATCTContent): #,journalcommons.BibDataMixin):
    """A book or object under review"""
    implements(IBookReview)

    meta_type = "BookReview"
    schema = BookReviewSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-


atapi.registerType(BookReview, PROJECTNAME)

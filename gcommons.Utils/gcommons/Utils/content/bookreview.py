"""Definition of the BookReview content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from gcommons.Core.widgets import FormAutoFillWidget 

from gcommons.Utils import UtilsMessageFactory as _
from gcommons.Utils.interfaces import IBookReview
from gcommons.Utils.config import PROJECTNAME

## Book Reviews
# Book Review Container: Folder, MailTemplatesContainer (or journal...)
#BookData
#Link reviewer, article, book data


BookReviewSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField('isbn',
        searchable=1,
        default='',
        is_duplicates_criterion=True,
        widget=FormAutoFillWidget(
            label="ISBN Number",
            label_msgid="label_isbn",
            description="The ISBN number of this publication.",
            description_msgid="help_isbn",
            helper_url='addbook_wizard'
        ),
    ),

    atapi.StringField('publisher',
                searchable=1,
                required=0,
                default='',
                is_duplicates_criterion=True,
                widget=atapi.StringWidget(label="Publisher",
                    label_msgid="label_publisher",
                    description="The publisher's name.",
                    description_msgid="help_publisher",
                    size=60,
                    i18n_domain="cmfbibliographyat",),
                ),
    atapi.StringField('address',
                searchable=1,
                required=0,
                default='',
                is_duplicates_criterion=True,
                widget=atapi.StringWidget(label="Address",
                    label_msgid="label_address",
                    description="Publisher's address. For major publishing houses, just the city is given. For small publishers, you can help the reader by giving the complete address.",
                    description_msgid="help_address",
                    size=60,
                    i18n_domain="cmfbibliographyat",),
                ),
))


def finalizeBookReviewSchema(schema):
    schema['title'].storage = atapi.AnnotationStorage()
    schema['description'].storage = atapi.AnnotationStorage()
    schemata.finalizeATCTSchema(schema, moveDiscussion=False)
    schema.moveField('isbn', before='title')
    return schema



class BookReview(base.ATCTContent): #,gcommons.BibDataMixin):
    """A book or object under review"""
    implements(IBookReview)

    meta_type = "BookReview"
    schema = finalizeBookReviewSchema(BookReviewSchema)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-


atapi.registerType(BookReview, PROJECTNAME)

"""Definition of the Draft content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from journalcommons.Journal import JournalMessageFactory as _
from journalcommons.Journal.interfaces import IDraft
from journalcommons.Journal.config import PROJECTNAME

DraftSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

DraftSchema['title'].storage = atapi.AnnotationStorage()
DraftSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(DraftSchema, moveDiscussion=False)

class Draft(base.ATCTContent):
    """File containing a draft of item"""
    implements(IDraft)

    meta_type = "Draft"
    schema = DraftSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Draft, PROJECTNAME)

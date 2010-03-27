"""Definition of the Section content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from journalcommons.Journal import JournalMessageFactory as _
from journalcommons.Journal.interfaces import ISection
from journalcommons.Journal.config import PROJECTNAME

SectionSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

SectionSchema['title'].storage = atapi.AnnotationStorage()
SectionSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    SectionSchema,
    folderish=True,
    moveDiscussion=False
)


class Section(folder.ATFolder):
    """A section of an issue in a journal"""
    implements(ISection)

    meta_type = "Section"
    schema = SectionSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(Section, PROJECTNAME)

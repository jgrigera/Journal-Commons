"""Definition of the SpecialIssue content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from gcommons.Journal import JournalMessageFactory as _
from gcommons.Journal.interfaces import ISpecialIssue
from gcommons.Journal.config import PROJECTNAME

# gcommons.Core
from gcommons.Core.lib.container import gcContainerMixin



SpecialIssueSchema = folder.ATFolderSchema.copy() + gcContainerMixin.schema.copy() + atapi.Schema((


))

def finalizeSpecialIssueSchema(schema):
    schema['title'].storage = atapi.AnnotationStorage()
    schema['description'].storage = atapi.AnnotationStorage()
    
    schemata.finalizeATCTSchema(schema, folderish=True, moveDiscussion=False)
    return schema

class SpecialIssue(gcContainerMixin, folder.ATFolder):
    """Special Issue or Research Thread"""
    implements(ISpecialIssue)

    meta_type = "SpecialIssue"
    schema = finalizeSpecialIssueSchema(SpecialIssueSchema)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    
atapi.registerType(SpecialIssue, PROJECTNAME)

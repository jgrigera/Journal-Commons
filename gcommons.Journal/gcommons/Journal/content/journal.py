"""Definition of the Journal content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from plone.app.folder import folder
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.lib import constraintypes

# gcommons.Core
from gcommons.Core.lib.container import gcContainerMixin

# gcommons.Journal
from gcommons.Journal import JournalMessageFactory as _
from gcommons.Journal.interfaces import IJournal
from gcommons.Journal.config import PROJECTNAME

#
# Schema
#
JournalSchema = folder.ATFolderSchema.copy() + gcContainerMixin.schema.copy() + atapi.Schema((
    atapi.StringField(
        name='issn',
        required=False,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        schemata ='bibdata',
        widget=atapi.StringWidget(
            label=_(u"ISSN"),
            description=_(u"Journal ISSN"),
        ),
    ),

    atapi.StringField(
        name='publisher',
        required=False,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        schemata ='bibdata',
        widget=atapi.StringWidget(
            label=_(u"Publisher"),
            description=_(u"Organization or company publishing the journal"),
        ),
    ),

    atapi.StringField(
        name='doiBase',
        required=False,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        schemata ='bibdata',
        widget=atapi.StringWidget(
            label=_(u"DOI Prefix"),
            description=_(u"Digital Object Identifier (DOI) Prefix"),
        ),
    ),

    atapi.StringField(
        name='additionalISSN',
        required=False,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        schemata ='bibdata',
        widget=atapi.StringWidget(
            label=_(u"Additional ISSN"),
            description=_(u"Additional ISSN, like Online ISSN"),
        ),
    ),

))


def finalizeJournalSchema(schema):
    schema['title'].storage = atapi.AnnotationStorage()
    schema['title'].widget.label = 'Name'
    schema['title'].widget.description = 'Type the name of the Journal'
    schema['description'].storage = atapi.AnnotationStorage()
    schemata.finalizeATCTSchema(schema,folderish=True,moveDiscussion=False)
    return schema


class Journal(gcContainerMixin,folder.ATFolder):
    """An object that will hold a Journal"""
    implements(IJournal)

    meta_type = "Journal"
    schema = finalizeJournalSchema(JournalSchema)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    publisher = atapi.ATFieldProperty('publisher')


atapi.registerType(Journal, PROJECTNAME)

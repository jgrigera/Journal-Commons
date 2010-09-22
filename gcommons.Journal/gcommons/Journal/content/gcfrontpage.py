"""Definition of the gcFrontPage content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from gcommons.Journal import JournalMessageFactory as _
from gcommons.Journal.interfaces import IgcFrontPage
from gcommons.Journal.config import PROJECTNAME

gcFrontPageSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.StringField(
        name='journal',
        required=False,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        schemata ='Journal',
        widget=atapi.StringWidget(
            label=_(u"Journal name"),
            description=_(u"Journal that will be published on the front page"),
        ),
    ),

    atapi.StringField(
        name='issueType',
        required=True,
        searchable=1,
        storage=atapi.AnnotationStorage(),
        vocabulary=((
                ('Issue', u'Issue'),
                ('SpecialIssue', u'Special Issue'),
                ('ResearchThread', u'Research Thread'),
                )), 
        enforceVocabulary=True,
        widget = atapi.SelectionWidget(            
            label="Issue Type",
            description="Select the type of issue",
            label_msgid="gc_issue_type",
            description_msgid="gc_help_issue_type",            
            i18n_domain="gcommons.Journal"
        ),
#        vocabulary=["Issue", "SpecialIssue", "ResearchThread"] 
    ),

    atapi.StringField(
        name='issueName',
        required=False,
        searchable=1,
        #default='',
        storage=atapi.AnnotationStorage(),
        schemata ='Journal',
        widget=atapi.StringWidget(
            label=_(u"Issue name"),
            description=_(u"Issue that will be published on the front page"),
        ),
    ),
))

# Set storage on fields copied from ATContentTypeSchema, making sure
# they work well with the python bridge properties.

gcFrontPageSchema['journal'].storage = atapi.AnnotationStorage()
gcFrontPageSchema['issueType'].storage = atapi.AnnotationStorage()
gcFrontPageSchema['issueName'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(gcFrontPageSchema, moveDiscussion=False)

class gcFrontPage(base.ATCTContent):
    """presentation on"""
    implements(IgcFrontPage)

    meta_type = "gcFrontPage"
    schema = gcFrontPageSchema

    journal = atapi.ATFieldProperty('journal')
    issueType = atapi.ATFieldProperty('issueType')
    issueName = atapi.ATFieldProperty('issueName')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(gcFrontPage, PROJECTNAME)

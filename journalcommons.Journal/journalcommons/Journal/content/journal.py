"""Definition of the Journal content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.lib import constraintypes

from journalcommons.Journal import JournalMessageFactory as _
from journalcommons.Journal.interfaces import IJournal
from journalcommons.Journal.config import PROJECTNAME

JournalSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
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

    atapi.LinesField(        
        name = 'editors',
        storage=atapi.AnnotationStorage(),
        widget = atapi.LinesWidget(            
            label="Editorial Board",            
            description="Enter the user ids of the users who compose the EB and are able to manage this journal, one per line.",            
            label_msgid='jcommons_label_editors',            
            description_msgid='jcommons_help_editors',            
            i18n_domain='journalcommons.Journal',        
        ),        
        default_method="getDefaultEditors"    
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

JournalSchema['title'].storage = atapi.AnnotationStorage()
JournalSchema['description'].storage = atapi.AnnotationStorage()
schemata.finalizeATCTSchema(
    JournalSchema,
    folderish=True,
    moveDiscussion=False
)


class Journal(folder.ATFolder):
    """Root for all files in a journal"""
    implements(IJournal)

    meta_type = "Journal"
    schema = JournalSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    publisher = atapi.ATFieldProperty('publisher')
    editors = atapi.ATFieldProperty('editors')
    # -*- Your ATSchema to Python Property Bridges Here ... -*-

    """
    Defaults
    """
    def getDefaultEditors(self):        
        """ 
        The default list of managers should include the tracker owner
        """        
        return (self.Creator(),)

    """
    Items to share with jcommons
    """
    def aq_getSubmissionsConfig(self):
        return Journal.config_Submissions
    
    def aq_getContainerName(self):
        return "Journal"
    def aq_getItemsName(self):
        return "Article"
    def aq_getItemsType(self):
        return "Article"
    def aq_stateDraftsAllowed(self):
        return True
    def aq_getEditorsList(self):
        return self.editors
    
    def at_post_create_script(self):
        """ Create a folder for Submissions
        """
        fldid = self.invokeFactory('SubmissionsFolder', 'submit', title = 'Submissions',
        			    description='This folder holds article submissions')

    config_Submissions = {
            'ContainerName':'Journal',
            'Items': [ { 'name': 'Article',
                         'type': 'Article',
                         'description': """Articles...
                                        """,
                         },
            ]
    }

atapi.registerType(Journal, PROJECTNAME)

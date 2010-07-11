"""Definition of the Journal content type
"""

import os
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.lib import constraintypes

from journalcommons.Journal import JournalMessageFactory as _
from journalcommons.Journal.interfaces import IJournal
from journalcommons.Journal.config import PROJECTNAME

from gcommons.Core.lib.gcommonsConfiguration import gcommonsConfiguration, readFile

# Validation
import gcommons.Core.validators  
from Products.validation import V_REQUIRED


#
# Schema
#
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


    atapi.FileField(
        name='configuration',
        required = False,
        searchable = False,
        languageIndependent = True,                   
        storage = atapi.AnnotationStorage(),
        default = readFile(os.path.dirname(__file__), 'journal.xcfg'),
        validators = (('isNonEmptyFile', V_REQUIRED), 
                      ('checkFileMaxSize', V_REQUIRED), # This comes from ATContentType.file
                      ('isValidXML', V_REQUIRED)),  
        widget=atapi.FileWidget (
                description='Configuration XML, please leave empty if you dont know what this means',
                label= 'Configuration XML'
        ),                 
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
    def parseConfiguration(self):
        xmlstring = str(self.configuration)
        dom = XMLParseString(xmlstring)
        self.parsedConfiguration = dom.documentElement
        
    def aq_getConfig(self):
        # TODO: Cache this parsing, by providing setter for configuration 
        self.parseConfiguration()
        return gcommonsConfiguration(parsedxml=self.parsedConfiguration)
    
    def aq_stateDraftsAllowed(self):
        return True
    
    def at_post_create_script(self):
        """ Create a folder for Submissions
        """
        fldid = self.invokeFactory('SubmissionsFolder', 'submit', title = 'Submissions',
        			    description='This folder holds article submissions')


atapi.registerType(Journal, PROJECTNAME)

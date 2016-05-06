
import os
import logging

from AccessControl import ClassSecurityInfo
from zope.event import notify
from zope.interface import implements
from Acquisition import aq_inner, aq_parent                       

# Plone
from Products.CMFCore.utils import getToolByName
from Products.Archetypes import atapi
from plone.memoize.instance import memoize, clearbefore
from archetypes.referencebrowserwidget import ReferenceBrowserWidget

# Core
from gcommons.Core.permissions import roles
from gcommons.Core.interfaces import IgcContainer, IgcContainerModifiedEvent 
from gcommons.Core.lib import is_gcommons_Users_installed
from gcommons.Core.lib.configuration import gcConfiguration
from gcommons.Core.lib.configuration import readFile 

# XML - rename to allow other implementations in the future 
from xml.dom.minidom import parseString as XMLParseString
from xml.parsers.expat import ExpatError as XMLError

# Validation
import gcommons.Core.validators  
from Products.validation import V_REQUIRED

from gcommons.Core import CoreMessageFactory as _


logger = logging.getLogger("gcommons.Core.lib.container")


#
# Schema
#
gcContainerSchema_base = atapi.Schema ((
    atapi.LinesField(        
        name = 'txtEditors',
        storage = atapi.AnnotationStorage(),
        widget = atapi.LinesWidget(            
            condition="here/condition_txtEditors",
            label="Editorial Board",    #Guest Editors/Comittee      
            description="Enter the user ids of the users who compose the EB and are able to manage this journal, one per line.",            
            label_msgid='gcommons_label_editors',            
            description_msgid='gcommons_help_editors',            
            i18n_domain='gcommons.Core',        
        ),        
        default_method="getDefaultEditors"    
    ),

    atapi.ReferenceField(
        name='refEditors',
        relationship = 'refEditors',
        required = False,
        multiValued = True,
        searchable=1,
        allowed_types=('gcPerson',),
        storage=atapi.AnnotationStorage(),
        
        widget = ReferenceBrowserWidget(
            condition="here/condition_refEditors",
            label=_("Editorial Board"),            
            description=_("Pick the users who compose the EB and are able to manage this journal/conf/RT."),            
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1, 
#            startup_directory_method="_get_gcommons_users_tool",
        ),            
    ),
    

    atapi.FileField(
        name='configuration',
        required = False,
        searchable = False,
        languageIndependent = True,
        storage = atapi.AnnotationStorage(),
        validators = (('isNonEmptyFile', V_REQUIRED), 
                      ('checkFileMaxSize', V_REQUIRED), # This comes from ATContentType.file
                      ('isValidXML', V_REQUIRED)),  
        widget = atapi.FileWidget (
                description='Configuration XML, please leave empty if you dont know what this means',
                label= 'Configuration XML'
        ),                 
        default_method = 'getDefaultConfiguration',
    ),
))


def finalizeContainerSchema(schema):
    # nothing now
    return schema


def gcommons_aq_container(context):
    """ Returns topmost gcContainer from context
    """
    if not IgcContainer.providedBy(context):
        parent = aq_parent(aq_inner(context))
        if parent is not None:
            return gcommons_aq_container(parent)
        else:
            return None
    else:
        return context    



class gcContainerModifiedEvent(object):
    """ Event that happens when edits to any gcContainer have been saved
    """
    implements(IgcContainerModifiedEvent)
    
    def __init__(self, context):                      
        self.context = context



class gcContainerMixin:
    """
    Class that holds common functions of containers (Journal, Conference, Book, SpeciallIssue/ResearchThread, etc) 
    """
    implements(IgcContainer)
    security = ClassSecurityInfo()

    schema = finalizeContainerSchema(gcContainerSchema_base)
    # Let others schemas order our chunk of fields
    firstField = 'editors'
    lastField = 'configuration'  

    # Binders for Schema
    editors = atapi.ATFieldProperty('editors')
    configuration = atapi.ATFieldProperty('configuration')

    """
    Handle conditions
    """ 
    def condition_refEditors(self):
        """ This checks whether to show the refEditors
        """
        if is_gcommons_Users_installed(self):
            return True
        else:
            return False


    def condition_txtEditors(self):
        """ Only show the txtEditors if no gcUsers
        """
        if is_gcommons_Users_installed(self):
            return False
        else:
            return True

    """
    Validators
    """
    def validate_txtEditors(self, value):
        """Make sure editors are actual user ids"""
        membership = getToolByName(self, 'portal_membership')
        notFound = []
        for userId in value:
            member = membership.getMemberById(userId)
            if member is None:
                notFound.append(userId)
        if notFound:
            return "The following user ids could not be found: %s" % ','.join(notFound)
        else:
            return None
        
    """
    Defaults
    """
    def getDefaultEditors(self):        
        """ 
        The default list of managers should include the tracker owner
        """        
        return (self.Creator(),)
    
    def getDefaultConfiguration(self):
        return readFile(os.path.dirname(__file__), '%s.xcfg' % self.meta_type)

    """
    Editors
    """
    def getEditors(self):
        """ Unified access to txt or ref editors
        """
        portal_membership = getToolByName(self, 'portal_membership')
        editors = []
        for userId in self.getTxtEditors():
            editors.append(portal_membership.getMemberById(userId))
        for obj in self.getRefEditors():
            member = portal_membership.getMemberById(obj.getId())
            editors.append(member)
        return editors
        
    def setTxtEditors(self, newEditors):
        field = self.getField('txtEditors')
        currentEditors = field.get(self)
        field.set(self, newEditors)
        self.updateEditors(currentEditors, newEditors)
    
    def setRefEditors(self, newEditorsUIDs):
        field = self.getField('refEditors')
        currentEditors = field.get(self)
        currentEditorsIds = [ user.getId() for user in currentEditors ]

        # newEditors now contiains UIDs of objects, let default setter resolve them 
        field.set(self, newEditorsUIDs)
        newEditors = field.get(self)
        newEditorsIds = [ user.getId() for user in newEditors ]

        self.updateEditors(currentEditorsIds, newEditorsIds)

    #TODO: security.declareProtected(ModifyPortalContent, 'setEditors')
    def updateEditors(self, currentEditors, newEditors):
        """
        Set the list of editors, and give them the EditorialBoard local role.
        taken from Poi.PoiTracker
        """
        toRemove = [m for m in currentEditors if m not in newEditors]
        
        for userId in toRemove:
            local_roles = list(self.get_local_roles_for_userid(userId))
            if roles.EditorialBoard in local_roles:
                local_roles.remove(roles.EditorialBoard)
                if local_roles:
                    # One or more roles must be given
                    self.manage_setLocalRoles(userId, local_roles)
                else:
                    self.manage_delLocalRoles(toRemove)

        for userId in newEditors:
            local_roles = list(self.get_local_roles_for_userid(userId))
            if not roles.EditorialBoard in local_roles:
                local_roles.append(roles.EditorialBoard)
                self.manage_setLocalRoles(userId, local_roles)
    
    """
    Configuration
    """
    def setConfiguration(self, *args, **kw):
        """ Provide a setter that clears the Cached parsed configuration value
        """
        # invalidate cache
        self.__getConfig_clear()
        # let default setter handle now
        field = self.getField('configuration')
        return field.set(self, *args, **kw)

    def parseConfiguration(self):
        xmlstring = str(self.configuration)
        dom = XMLParseString(xmlstring)
        self.parsedConfiguration = dom.documentElement

    @memoize        
    def aq_getConfig(self):
        self.parseConfiguration()
        return gcConfiguration(parsedxml=self.parsedConfiguration)
    
    @clearbefore
    def __getConfig_clear(self):
        """ Reset memoized value
        """
        logger.info("Cleaning memoized value")
        return None
    
    
    """
    Post Creation
    """    
    def at_post_edit_script(self):
        """Notify that the Person has been modified.
        """
        #NOTE: there is no subscriber to this event, so far
        notify(gcContainerModifiedEvent(self))

    def at_post_create_script(self):
        """ Create a folder for Submissions
        """
        logger.info("at_post_create_script Adding Submissions Folder to %s" % self.meta_type)
        fldid = self.invokeFactory('SubmissionsFolder', 'submit', title = 'Submissions',
                        description='This folder holds article submissions')
        #NOTE: there is no subscriber to this event, so far
        notify(gcContainerModifiedEvent(self))


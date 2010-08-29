


import logging
from operator import itemgetter

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Archetypes import atapi
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.DataGridField.DataGridWidget import DataGridWidget
from Products.DataGridField.DataGridField import DataGridField
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
#from gcommons.Core.widgets.ReferenceColumn import ReferenceColumn
from Products.DataGridField.HelpColumn import HelpColumn

# Maybe temp:
from gcommonsConfiguration import gcommonsRelatorType

from gcommons.Core import CoreMessageFactory as _


logger = logging.getLogger("gcommons.Core.lib.creators")


#
#
#
gcRelatorsSchema_base = atapi.Schema ((

    atapi.StringField(
        name='primaryAuthor',
        searchable=True,
        index='FieldIndex',
        default_method ='_compute_author',
        vocabulary = 'vocabAuthor',
        storage = atapi.AnnotationStorage(),
        widget = atapi.ComputedWidget(
            name = 'Primary Author',
            description = _('Principal creator or responsible of the paper.'),
            visible = {'edit' : 'visible', 'view' : 'visible' },
        ),
    ),

    # testing this

    # This field is used
    #    if gcommons.Users not installed, hidden
    #    if user registration enforced: to hold them after registered
#    DataGridField(
#        name='refRegisteredRelators',
#        widget=DataGridWidget(
#            label=_("Other Authors (Already Registered)"),
#            description = _('If applicable, other authors of the paper or persons responsible for this piece, besides the principal author.'),
#            columns={
#                'relationship': SelectColumn(_(u'Relation'), vocabulary="listRelatorTypes"),
#                'reference':    HelpColumn(_(u"Reference"), "Search here", "help", "info.gif"),    
#            },
#            condition="here/condition_registered"
#        ),
#        allow_empty_rows=False,
#        required=False,
#        columns=('relationship', 'reference')
#    ),

    atapi.ReferenceField(
        name='refRegisteredRelators',
        relationship = 'refRegisteredRelators',
        required = False,
        multiValued = True,
        searchable=1,
        allowed_types=('gcPerson',),
        storage=atapi.AnnotationStorage(),
        
        widget = ReferenceBrowserWidget(
            condition="here/condition_registered",
            label=_("Other Authors"),
            description = _('If applicable, other authors of the paper or persons responsible for this piece, besides the principal author. NOTE that they must be already registered with the site.'),
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1, 
#            startup_directory_method="_get_gcommons_users_tool",
        ),            
    ),

    # This field is used
    #    if invitations are allowed, and users enforced: to hold invitations, else hidden
    #    if gcommons.Users not installed, to hold users
    DataGridField(
        name='unregisteredRelators',
        widget=DataGridWidget(
            label=_("Other Authors"),
            condition="here/condition_unregistered",
            description = _('If applicable, other authors or contributors of the paper or persons responsible for this piece, besides the principal author.'),
            columns={
                'relationship': SelectColumn(_(u'Relation'), vocabulary="listRelatorTypes"),
                'name': Column(_(u'Name')),
                'institution': Column(_('Institution')),
                'email': Column(_('email')),
            },
        ),
        allow_empty_rows=False,
        required=False,
        columns=('relationship', 'name', 'institution', 'email')
    ),


    # Migration!!
    DataGridField(
        name='unconfirmedExtraAuthors',
        widget=DataGridWidget(
            label=_("Other Authors"),
            description = _('If applicable, other authors of the paper or persons responsible for this piece, besides the principal author.'),
            column_names=('Name', 'Institution', 'email'),
        ),
        mode = 'r',
        allow_empty_rows=False,
        required=False,
        columns=('name', 'institution', 'email')
    ),

   
    #
    # Overrride default fields creators and contributors
    atapi.ComputedField(
        name='creators',
        accessor='Creators',
        expression='context._compute_creators()',
        storage = atapi.AnnotationStorage(),
        searchable = True,
    ),
    atapi.ComputedField(
        name='contributors',
        accessor='Contributors',
        expression='context._compute_contributors()',
        storage = atapi.AnnotationStorage(),
        searchable = True,
    ),
))



def finalizeAuthorsSchema(schema):
    """
    fix and finish Authors Schema
    """

    # First of all, do we have gcommons.Users installed?
    try:
        from gcommons.Users.config import PROJECTNAME
    except ImportError:
        # gcommons.Users not around, so
        #     enforceRegistration not possible 
        #     invitations are not possible
        logger.info("gcommons.Users not found, disabling enforceRegistration and Invitations")

        #    TODO: in the future we could alllow referencing of plain Plone Users, thus allowing enforceRegistration
        logger.info("gcommons.Users invitations not possible")
        logger.info("gcommons.Users enforceRegistration not possible")
        # Make this dissapear, but dont delete it to save data (if there)
        schema['refRegisteredRelators'].mode='r'

    return schema



class RelatorsMixin:
    """
    Class that holds bunch of people related to an object submitted
    """
    
    schema = finalizeAuthorsSchema(gcRelatorsSchema_base)
    # Let others schemas order our chunk of fields
    firstField = 'primaryAuthor'
    lastField = 'unconfirmedExtraAuthors'  

    #
    # Widget Helpers:
    #     vocabularies, defaults, etc    
    def listRelatorTypes(self):
        context = aq_inner(self)
        config = context.aq_getConfig()
        configtype = config.getItemType_byPortalType(self.portal_type)
        
        return atapi.DisplayList([(relator.id(),relator.name()) for relator in  configtype.relators() ])

    def SearchAllUsers_refbrowser(self):
        """ return a query dictionary to limit the search parameters for a reference browser                                                                            
            widget query.                                                                                                 
        """                                                                                                                                                             
        return {'portal_type': 'gcPerson',                                                                                                                             
#                'sort_on': sort_on,                                                                                                                                     
                'path': {'query': self.getPhysicalPath()}
        }                                                                                                                                


    def vocabAuthor(self):
        user = self.portal_membership.getAuthenticatedMember()
        list = atapi.DisplayList()
        list.add(user.getId(), user.fullname)
        return list
    
    def vocabRelationship(self, relationid):
        context = aq_inner(self)
        config = context.aq_getConfig()
        configtype = config.getItemType_byPortalType(self.portal_type)
        return configtype.getRelator_byId(relationid)

    #
    #
    # Handle conditions 
    def condition_unregistered(self):
        """ This checks whether to show the unregisteredAuthors
        """
        if self.is_gcommons_Users_installed():
            return False
        else:
            return True


    def condition_registered(self):
        """ Only show the Referenced relators field if gcommons.Users installed
        """
        if self.is_gcommons_Users_installed():
            return True
        else:
            return False

    def is_gcommons_Users_installed(self):
        context = aq_inner(self)
        portal_quickinstaller = getToolByName(context, 'portal_quickinstaller')
        return portal_quickinstaller.isProductInstalled('gcommons.Users')

        
        
    #
    # Computed fields
    def _compute_author(self):
        user = self.portal_membership.getAuthenticatedMember()
        return user.getId()
    
    def _compute_creators(self):
        """ Join values of author and extra authors
        
        Caveat: order of evaluation in schema is relevant.
        """
        creators = []
        for author in self.getRelators(relationship='aut'):
            try:
                creators.append("%s (%s)" % (author['name'], author['institution']))
            except KeyError:
                pass
        return creators
        
    def _compute_contributors(self):
        contributors = []
        for contributor in self.getUnregisteredRelators():
            try:
                if contributor['relationship'] != 'aut':
                    contributors.append("%s (%s)" % (contributor['name'], contributor['relatonship']))
            except KeyError:
                pass
        return contributors

    
    #
    #
    # Getters
    def getRelators(self, relationship=None):
        """
        return a list of authors, translators, chairs, coordinators, etc for this piece
        
        format is a list of dictionaries containing name, relationship, institution
        """
        relators = []

        # primary Author
        portal_membership = getToolByName(self, 'portal_membership')
        
        primaryAuthor = self.getPrimaryAuthor() 
        member = portal_membership.getMemberById(primaryAuthor)
        homeUrl = portal_membership.getHomeUrl(primaryAuthor)

        # TODO this is quick fix if no relationship is found
        # probably a 'default' one could be specified in the XCFG
        default_relationship = gcommonsRelatorType(xmlnode = None, values={'marccode': 'aut', 'name':'Author', 'description':'Author', 'displayorder':0})
        
        relators.append({'id': primaryAuthor,
                         'name': member.getProperty('fullname'),
                         'homeurl': homeUrl,
                         'institution': "", #TODO: maybe this can be known if it is a gcUser
                         'relationship': default_relationship.name(),
                         'email': member.getProperty('email'),
                         'order': default_relationship.displayorder()
                         })

        user = self.portal_membership.getAuthenticatedMember()
        list = atapi.DisplayList()
        list.add(user.getId(), user.fullname)
        
        # unregistered
        for relator in self.getUnregisteredRelators():
            # Sometimes we get called before DataGrid is set
            if len(relator) < 1:
                continue
            
            relationship = self.vocabRelationship(relator['relationship'])
            if relationship is None:
                relationship = default_relationship
            
            relators.append({'id': relator['name'].replace(' ', '_'),
                             'name': relator['name'], 
                             'institution': relator['institution'],
                             'homeurl': None,
                             'relationship': relationship.name(),
                             'email':  relator['email'],
                             'order': relationship.displayorder()
                            })
        
        # registered
        for relator in self.getRefRegisteredRelators():
            # TODO: this should be fixed
            relationship = default_relationship
            relators.append({'id': relator.getId(),
                             'name': relator.Title(), 
                             'institution': "",#relator['institution'],
                             'homeurl': relator.absolute_url(),
                             'relationship': relationship.name(),
                             'email':  relator.getEmail(),
                             'order': relationship.displayorder()
                            })
            

        # sort them
        return sorted( relators, key=itemgetter('order'))

        
    def getRelators_text(self, relationship=None):
        """
        return a list of authors, translators, chairs, coordinators, etc for this piece
        but only as text
        
        """
        relators = self.getRelators()
        
        return 'TODO'




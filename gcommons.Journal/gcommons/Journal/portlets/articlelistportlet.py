from zope.interface import Interface
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.component import queryUtility

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from plone.memoize.instance import memoize
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

#TODO: should be this
#from gcommons.Journal.portlets import ArticleListPortletMessageFactory as _
from gcommons.Journal import JournalMessageFactory as _

class IArticleListPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    portlet_title = schema.TextLine( title=_(u'Title'),
        description=_(u'Title of the portlet..'),
        required=False,
        default=u'Article List'
        )
    watch_review_state = schema.Tuple(title=_(u"Workflow state"),
            description=_(u"Items in which workflow state to show."),                         
            default=('eb_draft', ),
            required=True,                         
            value_type=schema.Choice(                             
                    vocabulary="plone.app.vocabularies.WorkflowStates")                         
            )


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IArticleListPortlet)

    def __init__(self, portlet_title=_("Article List"), watch_review_state=("eb_draft",)):
        self.portlet_title = portlet_title
        self.watch_review_state = watch_review_state

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "Article list portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    render = ViewPageTemplateFile('articlelistportlet.pt')

    @property    
    def anonymous(self):        
        context = aq_inner(self.context)        
        portal_state = getMultiAdapter((context, self.request),                                       
                                       name=u'plone_portal_state')        
        return portal_state.anonymous()   

    @property    
    def title(self):
        """return title of feed for portlet"""
        return getattr(self.data, 'portlet_title', _('Article List'))
    
    @property    
    def available(self):        
        """ Show only for logged in users and when data is available """
        return True
        #return not self.anonymous and len(self._data())

    def full_list_link(self):
        """ 
        Return link to full list of items in state x
        """        
        context = aq_inner(self.context)        
        portal_state = getMultiAdapter((context, self.request),                                       
                                       name=u'plone_portal_state')
        # TODO: not this..        
        return '%s/full_review_list' % portal_state.portal_url()

    def articlelist_items(self):
        return self._data()

    @memoize    
    def _data(self):        
        """ Get list of objects to be shown """
        if self.anonymous:            
            return []        
        context = aq_inner(self.context)        
        workflow = getToolByName(context, 'portal_workflow')
        portal_catalog = getToolByName(self, 'portal_catalog')
        
        plone_view = getMultiAdapter((context, self.request), name=u'plone')        
        getIcon = plone_view.getIcon        
        toLocalizedTime = plone_view.toLocalizedTime


        idnormalizer = queryUtility(IIDNormalizer)       
        norm = idnormalizer.normalize        
        # TODO:
        # This is clever, but in the future...
        #objects = workflow.getWorklistsResults()        

        items = []       
        for obj in portal_catalog.searchResults(portal_type='Article', review_state=self.data.watch_review_state,
                                                sort_on='sortable_title'):
            #review_state = workflow.getInfoFor(obj, 'review_state')            
            items.append(dict(                
                    #path = obj.absolute_url,
                    path = obj.getURL(),                
                    title = obj.pretty_title_or_id,                
                    description = obj.Description,                
                    icon = getIcon(obj).html_tag(),                
                    creator = obj.Creator,                
                    review_state = obj.review_state,                
                    review_state_class = 'state-%s ' % norm(obj.review_state),                
                    mod_date = toLocalizedTime(obj.ModificationDate),
            ))
        return items
        



class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IArticleListPortlet)
    label = _(u"Add Article List Portlet")    
    description = _(u"This portlet lists articles in a certain workflow state.")

    def create(self, data):
        return Assignment(portlet_title=data.get('portlet_title',_("Article List")), watch_review_state=data.get('watch_review_state', ('eb_draft',)))


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IArticleListPortlet)
    label = _(u"Add Article List Portlet")    
    description = _(u"This portlet lists articles in a certain workflow state.")

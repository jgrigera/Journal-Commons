from zope.interface import implements, Interface
from Products.CMFCore.utils import getToolByName

from gcommons.Core import CoreMessageFactory as _
from gcommons.Core.browser import gcommonsView 

import logging
logger = logging.getLogger('gcommons.Core.browser.subissionseditorsview')



class ISubmissionsEditorsView(Interface):
    """
    SubmissionsEditors view interface
    """

    def getSubmissionsByState():
        """ Return a list of available states for item contained
            and the quantity
        """

class ISubmissionsAsExcelView(Interface):
    """
    SubmissionsEditors view interface
    """


class SubmissionsEditorsView(gcommonsView):
    """
    SubmissionsEditors browser view
    This allows editors to have an overview of current submissions status
    """
    implements(ISubmissionsEditorsView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def portal_workflow(self):
        return getToolByName(self.context, 'portal_workflow')

    def getSubmittablePortalTypes(self):
        """
        Read container configuration
        """
        config = self.context.aq_getConfig()
        return [item.portal_type() for item in config.getSubmittableItems()]
    #
    # portal_catalog queries
    def getSubmissionsByType(self):
        types = []
        config = self.context.aq_getConfig()
        for item in config.getSubmittableItems():
            types.append({'id': item.portal_type(),
                           'title': item.name(),
                           'description': item.description(),
                           'quantity': len(self.getSubmissions(portal_type=item.portal_type()))})
        return types    
    
    def getSubmissionsBySubtype(self, type):
        subtypes = []
        config = self.context.aq_getConfig()
        for item in config.getItemType_byPortalType(type).subtypes():
            subtypes.append({'id': item.id(),
                           'title': item.name(),
                           'description': item.description(),
                           'quantity': len(self.getSubmissions(portal_type=type, get_item_subtype=item.id()))
            })
        return subtypes    
        
    
    def getSubmissionsByState(self):
        """ Return a list of available states for item contained
            and the quantity
        """
        # Get the workflow of the items added here
        states = []
        
        # Get a list of all relevant states
        # getChainForPortalType returns a list of workflow ids applicable to portal_type
        wf_states = {}
        for portal_type in self.getSubmittablePortalTypes():
            for state in self.portal_workflow.getChainForPortalType(portal_type):
                wf_states[state] = state
        
        for wf_id in wf_states.keys():
            workflow = self.portal_workflow.getWorkflowById(wf_id)
            for strstate in workflow.states:
                state = workflow.states.get(strstate)
                states.append({'id': state.getId(),
                               'title': state.title,
                               'description': state.description,
                               'quantity': len(self.getSubmissions(state=state.getId()))})
        return states

    def getSubmissionsByAction(self):
        """ Return a list of available states 
        """
        states = []
        # Action is either by
        #TODO: improve this logic
        wf_states = []
        for portal_type in self.getSubmittablePortalTypes():
            for state in self.portal_workflow.getChainForPortalType(portal_type):
                wf_states.append(state)
        wf_states.sort()
        
        for wf_id in wf_states:
            workflow = self.portal_workflow.getWorkflowById(wf_id)
            for strstate in workflow.states:
                state = workflow.states.get(strstate)
                if strstate=='eb_draft':
                    title='Editorial Board'
                    description="Awaiting action from the EB"
                elif strstate=='draft':
                    title='Author'
                    description="Awaiting action from the author"
                elif strstate=='referee_draft':
                    title='Referees'
                    description="Awaiting action from the referees"
                else:
                    continue
                states.append({'id': state.getId(),
                           'title': title,
                           'description': description,
                           'quantity': len(self.getSubmissions(state=state.getId()))})
                    
        return states
    
    def getSubmissions(self, **kw):
        return self.context.searchSubmissions(**kw)


    def extraActions(self):
        results = []
        results.append( {   'url': 'gcommons_submissions_asxls_view', 
                            'icon':  'download_icon.gif',
                            'title':'Download list of submissions as Excel',} )
        return results


class SubmissionsAsExcelView(gcommonsView):
    implements(ISubmissionsAsExcelView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """
        This method gets called everytime the template needs to be rendered
        """
        self.request.RESPONSE.setHeader('Content-Type','application/excel')
        self.request.RESPONSE.addHeader("Content-Disposition","filename=%s.xls" % self.context.Title())
        self.request.RESPONSE.write( self.context.download_all_as_excel().getvalue() )
        return 
    

from zope.interface import implements, Interface
from Products.CMFCore.utils import getToolByName

from journalcommons.Journal import JournalMessageFactory as _
# CORE
from journalcommons.Journal.browser import jcommonsView 

import logging
logger = logging.getLogger('journalcommons.Journal.browser.subissionseditorsview')



class ISubmissionsEditorsView(Interface):
    """
    SubmissionsEditors view interface
    """

    def getSubmissionsByState():
        """ Return a list of available states for item contained
            and the quantity
        """



class SubmissionsEditorsView(jcommonsView):
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

    def getSubmissionsByType(self):
        pass
    
    
    def getSubmissionsByState(self):
        """ Return a list of available states for item contained
            and the quantity
        """
        # Get the workflow of the items added here
        states = []
        # getChainForPortalType returns a list of workflow ids applicable
        workflows = self.portal_workflow.getChainForPortalType(self.context.aq_getItemsType())
        for wf_id in workflows:
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
        workflows = self.portal_workflow.getChainForPortalType(self.context.aq_getItemsType())
        for wf_id in workflows:
            workflow = self.portal_workflow.getWorkflowById(wf_id)
            for strstate in workflow.states:
                state = workflow.states.get(strstate)
                if strstate=='eb_draft':
                    title='Editorial Board'
                elif strstate=='draft':
                    title='Author'
                elif strstate=='referee_draft':
                    title='Referees'
                else:
                    continue
                states.append({'id': state.getId(),
                           'title': title,
                           'description': state.description,
                           'quantity': len(self.getSubmissions(state=state.getId()))})
                    
        return states
    
    def getSubmissions(self, state=None):
        # maybe...
        #brains = self.context.listFolderContents(contentFilter={"portal_type" : "Article"})
        brains = self.portal_catalog({'portal_type': self.context.aq_getItemsType(),
                             'review_state': state,
                             'sort_on':'created',
                             'sort_order': 'reverse',
                             'path': '/'.join(self.context.getPhysicalPath())
                             })
        return brains

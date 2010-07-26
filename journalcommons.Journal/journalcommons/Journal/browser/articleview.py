# -*- coding: utf-8 -*-
from zope.interface import implements, Interface, alsoProvides

from plone.app.layout.globals.interfaces import IViewView

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

##TODO from collective.contacts import contactsMessageFactory as _

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IArticleView(Interface):
    """
    Article view interface
    """
    def get_user_details():
	"""return user details"""

    def get_drafts():
	"""return list of drafts"""


class ArticleView(BrowserView):
    """
    Article browser view
    """
    implements(IArticleView)

    pt = ViewPageTemplateFile('templates/jcommons_article_view.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """
        This method gets called everytime the template needs to be rendered
        """
        # This is needed so the actions bar will be shown.
        # the one with the actions, display, add item and workflow drop downs.
        portal_membership = getToolByName(self.context, 'portal_membership')
        if not portal_membership.isAnonymousUser():
            alsoProvides(self, IViewView)

        return self.pt()
    
    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def portal_workflow(self):
        return getToolByName(self.context, 'portal_workflow')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def get_drafts(self):
        """
        This method returns all drafts for this article
        """
        return self.context.get_drafts()
    
    def get_comments(self, draftid):
        """
        Return comments for draftid, in a dictionary containing
        type: (list, of, comments)
        """
        if draftid == 'current':
            pass
            #TODO: fix this
            
        # Get comments
        comments = self.context.listFolderContents(contentFilter={"portal_type" : ('Comment',)})
                
        # Order them by type, in a dictionary
        comments_by_type = {}
        for c in comments:
            try:
                comments_by_type[c.getCommentType()].append(c)
            except KeyError:
                comments_by_type[c.getCommentType()] = [c,]
            
        return comments_by_type
        

    def get_actions(self):
        """
        This method
        """
    	results = []
        drafts_allowed = self.context.aq_stateDraftsAllowed()
        #TODO: check permissions
        #tal:condition="python: checkPermission('Modify Portal Content', context)
    
    	review_state = self.portal_workflow.getInfoFor(self.context, 'review_state');
    	if review_state == 'draft':
            results = []
            if drafts_allowed:
                results.append( {   'url': 'createObject?type_name=Draft', 
                    			    'icon':  'upload_icon.gif',
                    			    'title':'Add a draft',} )
                extra = 'metadata'
            else:
                extra = 'abstract'
                
            results.append(	{   'url':  'edit',
                			    'icon': 'edit.gif',
                			    'title': 'Edit %s' % extra }  )
    			
    	    if len(self.get_drafts()) > 0 or (not drafts_allowed):
    		results.append(
    			{   'url':     'jc_content_submittoeb_form', 
    			    'title': 'Submit to editors',
    			    'icon':	'action_icon.gif',}
    			)
            return results

    def get_disable_border(self):
    	review_state = self.portal_workflow.getInfoFor(self.context, 'review_state');
    	if review_state == 'draft':
    	    return 1
    	if review_state == 'eb_draft' and not self.portal_membership.checkPermission('Modify Portal Content', self.context):
    	    return 1
    	return 0

	

    
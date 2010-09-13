# -*- coding: utf-8 -*-
from DateTime import DateTime
from zope.interface import implements, Interface, alsoProvides

from plone.app.layout.globals.interfaces import IViewView

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from gcommons.Core import permissions
from gcommons.Core.lib.gctime import gcommons_userfriendly_date
import logging

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
logger = logging.getLogger("gcommons.Journal.browser.articleview")


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

    pt = ViewPageTemplateFile('templates/gcommons_article_view.pt')

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
    def portal_actions(self):
        return getToolByName(self.context, 'portal_actions')

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

    """
    Draft 
    """
    def get_drafts(self):
        """
        This method returns all drafts for this article
        """
        return self.context.get_drafts()
    
    def are_drafts_allowed(self):
        return self.portal_membership.checkPermission(permissions.AddDraft, self.context)

    def get_draft_modification_date(self, draft, full=False):
        modificationdate = draft.ModificationDate()
        if full:
            return "%s (%s)" % (DateTime(modificationdate).strftime("%a %d %b %Y"),
                                gcommons_userfriendly_date(draft.ModificationDate()))
        else:
            return "%s" % DateTime(modificationdate).strftime("%a %d %b %Y")
        
    
    """
    Comments
    """
    def get_comments_by_type(self, draftid):
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
        for action_id in  self.portal_actions.listFilteredActionsFor(object=self.context)["gcommons_article_actions"]:
             results.append(action_id)
        return results


    def get_disable_border(self):
        review_state = self.portal_workflow.getInfoFor(self.context, 'review_state');
        if review_state == 'draft':
            return 1
        if review_state == 'eb_draft' and not self.portal_membership.checkPermission('Modify Portal Content', self.context):
            return 1
        return 0

    # TODO: this is not working. Move to workflow / object?
    def available_submittoeb(self):
        """ unsure whether this goes here or elsewhere
        """
        if len(self.get_drafts()) > 0 or (not self.are_drafts_allowed()):
            return True
        else:
            return False


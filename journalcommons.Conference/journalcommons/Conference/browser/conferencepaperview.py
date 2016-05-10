# -*- coding: utf-8 -*-
from DateTime import DateTime

from zope.interface import implements, Interface, alsoProvides
from zope.component import getMultiAdapter, queryMultiAdapter

from plone.app.layout.globals.interfaces import IViewView
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

# z3c.form
from Acquisition import aq_inner
from plone.z3cform.interfaces import IWrappedForm
from plone.z3cform import z2
from z3c.form.interfaces import IFormLayer

# gcommons
from gcommons.Core import permissions
from gcommons.Core.lib.gctime import gcommons_userfriendly_date
from gcommons.Core.lib.container import gcommons_aq_container

import logging
logger = logging.getLogger("gcommons.Conference.browser.conferencepaperview")


class IConferencePaperView(Interface):
    """
    ConferencePaper view interface
    """
    def get_user_details():
        """return user details"""
    
    def get_drafts():
        """return list of drafts"""

#
#
# TEMP HACK TO TEST SOMETHING
#
from gcommons.Journal.browser.forms.articleassigneditor import AssignEditorForm

class InlineFormActionView:
    def __init__(self, values, context=None, request=None):
        self.values = values

        self.form = AssignEditorForm(aq_inner(context), request)
        z2.switch_on(self.form, request_layer=IFormLayer)
        alsoProvides(self.form, IWrappedForm)

        self.form.update()
        self.values["form"] = self.form.render()

    def __call__(self):
        return """
<script type="text/javascript">
jQuery(document).ready(function(){
    $('.quick-actions-inline').click(function() {
        $(this).next().toggle('slow');
        return false;
    }).next().hide();
});
</script>
           <a class="quick-actions-inline"
              href="%(url)s" title="%(description)s">
              <img alt="*" src="%(icon)s"/> %(title)s
           </a>
           <div>%(form)s</div>
        """ % self.values


class SimpleActionView:
    def __init__(self, values, context=None, request=None):
        self.values = values

    def __call__(self):
        return """<a href="%(url)s" title="%(description)s"> <img alt="*" src="%(icon)s"/> %(title)s</a>""" % self.values

class WorkflowActionView:
    def __init__(self, values, context=None, request=None):
        self.values = values

    def __call__(self):
        return """<a href="%(url)s" title="Workflow Transition"> <img alt="*" src="action_icon.gif"/> %(title)s</a>""" % self.values



class ConferencePaperView(BrowserView):
    """
    ConferencePaper browser view
    """
    implements(IConferencePaperView)

    pt = ViewPageTemplateFile('templates/gcommons_conferencepaper_view.pt')

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

    def getLetterUrl(self):
        container = gcommons_aq_container(self.context)
        return "%s/Letter.doc" % container.absolute_url()

    """
    Draft 
    """
    def get_drafts(self):
        """
        This method returns all drafts for this ConferencePaper
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
        for action_id in self.portal_actions.listActionInfos(object=self.context, check_permissions=1, check_condition=1):
            if action_id['category'] == 'object_quick_article_actions':
                #if action_id['url'][0] == '#':
                #    results.append(InlineFormActionView(action_id, context=self.context, request=self.request))
                #else:
                results.append(SimpleActionView(action_id))
                    
        # Now add workflow actions
        locking_info = queryMultiAdapter((self.context, self.request), name='plone_lock_info')
        if locking_info and locking_info.is_locked_for_current_user():
            return results
        
        workflowActions = self.portal_workflow.listActionInfos(object=self.context)
        for action in workflowActions:
            logger.info(action)
            if action['category'] == 'workflow':
                results.append(WorkflowActionView(action))

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




from AccessControl import getSecurityManager                                                                                                                    
from Acquisition import aq_inner                                                                                                                                
                                                                                                                                                                
from zope.component import getMultiAdapter, queryMultiAdapter                                                                                                   
from plone.memoize.instance import memoize                                                                                                                      
                                                                                                                                                                
from plone.app.layout.viewlets import ViewletBase                                                                                                               
                                                                                                                                                                
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile                                                                                         
from Products.CMFCore.utils import _checkPermission                                                                                                             
from Products.CMFCore.utils import getToolByName                                                                                                                
from Products.CMFEditions.Permissions import AccessPreviousVersions                                                                                             
                                                                                                                                                                
from Products.CMFPlone import PloneMessageFactory as _                                                                                                          
                                                                                                                                                                
from Products.CMFCore.WorkflowCore import WorkflowException                                                                                                     
from Products.CMFPlone.utils import log                                                                                                                         
import logging                                                                                                                                                  
                                                                                                                                                                

                                                                                                                                                                

class AllRelatorsViewlet(ViewletBase):                                                                                                                       
    def update(self):                                                                                                                                           
        super(AllRelatortsViewlet, self).update()                                                                                                             
        self.context_state = getMultiAdapter((self.context, self.request),                                                                                      
                                             name=u'plone_context_state')                                                                                       
        self.tools = getMultiAdapter((self.context, self.request),                                                                                              
                                     name='plone_tools')                                                                                                        

    index = ViewPageTemplateFile("templates/gcommons_relators_provider.pt")                                                                                                          
  
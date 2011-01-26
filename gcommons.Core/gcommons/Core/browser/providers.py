

from zope.component import getMultiAdapter
                                                                                                                                                    
from plone.app.layout.viewlets import ViewletBase                                                                                                               
                                                                                                                                                                
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile                                                                                         
import logging                                                                                                                                                  
                                                                                                                                                                

                                                                                                                                                                

class AllRelatorsViewlet(ViewletBase):                                                                                                                       
    index = ViewPageTemplateFile("templates/gcommons_relators_provider.pt")                                                                                                          

    def update(self):                                                                                                                                           
        super(AllRelatorsViewlet, self).update()                                                                                                             
        self.context_state = getMultiAdapter((self.context, self.request),                                                                                      
                                             name=u'plone_context_state')                                                                                       
        self.tools = getMultiAdapter((self.context, self.request),                                                                                              
                                     name='plone_tools')                                                                                                        

  


import logging
import zope.thread                                
from Acquisition import aq_inner, aq_parent                       

from smtplib import SMTPRecipientsRefused
from Products.CMFCore.interfaces import ISiteRoot          
from Products.CMFCore.utils import getToolByName                                                                                     
from Products.Archetypes.interfaces import IBaseObject                                                                    
from Products.Archetypes.interfaces import IObjectInitializedEvent      

import gcommons.Core.actions as actions 

 
logger = logging.getLogger('gcommons.Core.subscribers')


# A thread local for keeping track of rule execution across events
_status = zope.thread.local()
      
def init():
    if not hasattr(_status, 'delayed_events'):
        _status.delayed_events = {}
                                                                                                                                                                                                
def is_portal_factory(context): 
    """Find out if the given object is in portal_factory, i.e. temporary object
    """
    portal_factory = getToolByName(context, 'portal_factory', None) 
    if portal_factory is not None:                                  
        return portal_factory.isTemporary(context)                 
    else:
        return False    

#TODO: move this funcition to some general util
def gcommons_aq_container(context):
    # Do not bubble beyond the gcommons Container (be it Conference, Thread, Journal)
    """
    if not IgcommonsContainer.providedBy(context):
        parent = aq_parent(aq_inner(context))
        while parent is not None:
            executor = IRuleExecutor(parent, None)
            if executor is not None:               
                executor(event, bubbled=True, rule_filter=rule_filter)
    TODO:
    """  
    pass
    
    
def get_gcommons_type_config(context, portal_type):
    """ Find out if portal_type is handled by our container
    """
    # TODO: is there a way to buble here finding out top container?
    #something = gcommons_aq_container(gcommons.IContainer)
    try:
        config = context.aq_getConfig()
        return config.getItemType_byPortalType(portal_type) 
    except AttributeError:
        # workaround until we have gcommons_aq_container
        return None

        

def triggerActions(context, eventid, object):

    typeconfig = get_gcommons_type_config(context, object.portal_type)
    if typeconfig is not None:
        notification = typeconfig.getNotification_byId(id=eventid)
        if notification is not None:
            logger.info("NOTIFICATION : %s" % notification.type())
            # notification.type() ... only mail now
            try:
                action = actions.mail(context=context, object=object, template=notification.template())
                action.execute()
            except AttributeError, e:
                logger.error("Some error here, %s" % e)
            except SMTPRecipientsRefused, e:
                logger.error("wrong email address %s" % e)
                

def archetypes_initialized(event):        
    """
        Pick up the delayed IObjectInitializedEvent when an Archetypes object is      
        initialized.    
        
        for "Products.Archetypes.interfaces.IObjectInitializedEvent"                                                                                                                                    
    """                                                                                  
    if is_portal_factory(event.object):                                             
        return                                                                             

    if not IBaseObject.providedBy(event.object):                                
        return                                

    context = aq_parent(aq_inner(event.object))
    triggerActions(context, 'created', event.object)
                                                                                                                   
                                                                                                                   
def workflow_action(event):
    """
        When a workflow action is invoked on an object, execute rules assigned 
        to its parent.
        
        for "Products.CMFCore.interfaces.IActionSucceededEvent"
    """
    if is_portal_factory(event.object):
        return
    
    context = aq_parent(aq_inner(event.object))
    triggerActions(context, 'workflow:%s' % event.action, event.object)

                



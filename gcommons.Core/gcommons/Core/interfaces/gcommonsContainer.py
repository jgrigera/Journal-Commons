
from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers



class IgcommonsContainer(Interface):
    """Any kind of item that can be handled in a Submissions Folder"""
    def aq_getConfig(self):
        """
        Return configuration object containing all relevant info on types and subtypes
        of items that can be added to this container
        
        retunr a gcommonsConfiguration object (or its interface) 
        """
        
        
    def aq_getAvailableSubcontainers(self, type_container=None, type_addable=None):
        """
        Return a list of available subcontainers (such ass Issues, Panels, events, etc).
        type_container is the type of containers targetted
        and type_addable is the type of object wished to be added
        """
        
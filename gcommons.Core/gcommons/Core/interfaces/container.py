
from zope import schema
from zope.interface import Interface, Attribute

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers



class IgcContainer(Interface):
    """Any kind of item that can be handled in a Submissions Folder"""
    def aq_getConfig(self):
        """
        Return configuration object containing all relevant info on types and subtypes
        of items that can be added to this container
        
        returns a gcommons.Core.lib.configuration object (or its interface) 
        """
        
        
    def aq_getAvailableSubcontainers(self, type_container=None, type_addable=None):
        """
        Return a list of available subcontainers (such ass Issues, Panels, events, etc).
        type_container is the type of containers targetted
        and type_addable is the type of object wished to be added
        """


class IgcContainerModifiedEvent(Interface):
    """An event fired when a person object is saved.
    """
    context = Attribute("The content object that was saved.")
        
from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from journalcommons.Conference import ConferenceMessageFactory as _
#from journalcommons.Core.interfaces import IjCommonsContainer
 #(IjCommonsContainer):
 
class IConference(Interface):
    """A container for the Conference"""
    
    # -*- schema definition goes here -*-

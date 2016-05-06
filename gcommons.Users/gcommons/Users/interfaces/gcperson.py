from zope import schema
from zope.interface import Interface, Attribute

from gcommons.Users import UsersMessageFactory as _

class IgcPerson(Interface):
    """A user of gcommons"""
    
    # -*- schema definition goes here -*-



class IgcPersonModifiedEvent(Interface):
    """An event fired when a person object is saved.
    """
    
    context = Attribute("The content object that was saved.")

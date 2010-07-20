from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from gcommons.Users import UsersMessageFactory as _

class IgcUserContainer(Interface):
    """A user container for gcommons.Users"""
    
    # -*- schema definition goes here -*-

from zope import schema
from zope.interface import Interface

from zope.container.constraints import contains
from zope.container.constraints import containers

from gcommons.Core import CoreMessageFactory as _

class IComment(Interface):
    """Object containing comments for an article"""
    
    # -*- schema definition goes here -*-

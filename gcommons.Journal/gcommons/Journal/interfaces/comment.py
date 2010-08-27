from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from gcommons.Journal import JournalMessageFactory as _

class IComment(Interface):
    """Object containing comments for an article"""
    
    # -*- schema definition goes here -*-

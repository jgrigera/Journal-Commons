from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from gcommons.Journal import JournalMessageFactory as _

class IDraft(Interface):
    """File containing a draft of item"""
    
    # -*- schema definition goes here -*-

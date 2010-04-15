from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from journalcommons.Journal import JournalMessageFactory as _

class IResearchThread(Interface):
    """Research Thread"""
    
    # -*- schema definition goes here -*-

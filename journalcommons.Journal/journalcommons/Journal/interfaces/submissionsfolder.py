from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from journalcommons.Journal import JournalMessageFactory as _

class ISubmissionsFolder(Interface):
    """Large folder to hold all pending Journal Submissions"""
    
    # -*- schema definition goes here -*-

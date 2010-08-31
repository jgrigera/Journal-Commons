from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from gcommons.Journal import JournalMessageFactory as _

class ISpecialIssue(Interface):
    """Special Issue or Research Thread"""
    
    # -*- schema definition goes here -*-

from zope import schema
from zope.interface import Interface

from journalcommons.Conference import ConferenceMessageFactory as _

class IConferencePaper(Interface):
    """A paper submitted to a conference"""
    
    # -*- schema definition goes here -*-

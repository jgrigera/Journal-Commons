from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from journalcommons.Conference import ConferenceMessageFactory as _

class IConferencePayment(Interface):
    """Registration and payment for conference"""
    
    # -*- schema definition goes here -*-

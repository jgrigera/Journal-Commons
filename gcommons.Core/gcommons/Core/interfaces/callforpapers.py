from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from gcommons.Core import CoreMessageFactory as _

class ICallForPapers(Interface):
    """Call for papers"""
    
    # -*- schema definition goes here -*-

from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from gcommons.Utils import UtilsMessageFactory as _

class IBookReview(Interface):
    """A book or object under review"""
    
    # -*- schema definition goes here -*-

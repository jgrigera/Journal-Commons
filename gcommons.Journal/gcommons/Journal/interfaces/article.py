from zope import schema
from zope.interface import Interface

from gcommons.Journal import JournalMessageFactory as _


class IArticle(Interface):
    """An article in an issue of a journal"""

    # -*- schema definition goes here -*-

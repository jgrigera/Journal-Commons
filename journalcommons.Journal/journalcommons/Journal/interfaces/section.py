from zope import schema
from zope.interface import Interface

from journalcommons.Journal import JournalMessageFactory as _


class ISection(Interface):
    """A section of an issue in a journal"""

    # -*- schema definition goes here -*-

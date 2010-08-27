from zope import schema
from zope.interface import Interface

from gcommons.Journal import JournalMessageFactory as _


class IJournal(Interface):
    """Root for all files in a journal"""

    # -*- schema definition goes here -*-

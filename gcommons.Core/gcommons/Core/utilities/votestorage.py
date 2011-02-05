
from zope.interface import implements

from persistent import Persistent
from persistent.dict import PersistentDict

from gcommons.Core.interfaces.utilities import IVoteStorage


class VoteStorage(Persistent):
    implements(IVoteStorage)

    def __init__(self):
        self.polls = PersistentDict()

    def vote(self, where, who, what):
        """ Store a vote
            where should be UID of poll
            who should be UID of user voting
            what is the vote
        """
        if not self.polls.has_key(where):
            self.polls[where] = PersistentDict()
            
        poll = self.polls[where]
        poll[who] = what
        
    def has_voted(self,where,who):
        try: 
            poll = self.polls[where]
            return poll.has_key(who)
        except KeyError:
            return False
    
    def get_vote(self,where,who):
        try: 
            poll = self.polls[where]
            return poll[who]
        except KeyError:
            #TODO: exception!
            return False
            
    def get_votes(self,where):
        try:
            return self.polls[where]
        except KeyError:
            return None
            

#
# if we create the utility with object= and using toolset.xml, then
# this wrapper is used
# good side of this is having tool in ZMI
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import registerToolInterface
from Products.CMFCore.utils import UniqueObject
from App.class_init import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

class VoteStorageTool(VoteStorage, UniqueObject, SimpleItem):
    """ This tool exposes the Vote Storage TTW
    """

    id = 'gcommons_votestorage'
    meta_type= 'gcommons Vote Storage Tool'
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        super(VoteStorageTool, self).__init__()

        self.id = id
        self.title = title

    manage_options=(
        {'label':'Dump', 'action':'manage_dumpVotesForm'},
        ) + SimpleItem.manage_options

    security.declareProtected(permissions.ManagePortal, 'manage_dumpVotesForm')
    manage_dumpVotesForm = PageTemplateFile('www/manage_dumpVotesForm', globals(),
        __name__='manage_dumpVotesForm')

    def dump_getPolls(self):
        return self.polls.keys()


InitializeClass(VoteStorageTool)
registerToolInterface('gcommons_votestorage', IVoteStorage)

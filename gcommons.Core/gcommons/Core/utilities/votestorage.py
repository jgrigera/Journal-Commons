
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
        
        
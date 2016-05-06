


from zope import schema
from zope.interface import Interface, Attribute



class IVoteStorage(Interface):

    def vote(where,who,what):
        """
        """
  
    def has_voted(where,who):
        """
        """
        
    def get_vote(where,who):
        """
        """

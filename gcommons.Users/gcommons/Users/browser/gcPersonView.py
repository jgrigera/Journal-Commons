from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from gcommons.Users import UsersMessageFactory as _


class IgcPersonView(Interface):
    """
    gcPerson view interface
    """


class gcPersonView(BrowserView):
    """
    gcPerson browser view
    """
    implements(IgcPersonView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def getSpamProtectedEmail(self):
        """
        return email protected agains scrapers
        """
        email = self.context.getEmail()
        
        # if obfuscate:                                                                                                                                    
        email = email.replace('.', ' [ DOT ] ')                                                                                                                             
        email = email.replace('@', ' [ AT ] ')                                                                                                                              
        email = email.replace('-', ' [ DASH ] ')                                                                                                                            
        email = email.replace('_', ' [ UNDERSCORE ] ')                                                                                                                      
        return email                                                                                                                                                        
        #else:                                                                                                                                                                   
        #    return self.context.spamProtect(email)                                                                                                                                   

    def get_your_contributions(self, type):
        """
        This method returns all items of type 'type' for currently logged in user
        """
        user = self.portal_membership.getAuthenticatedMember()
        user_id = user.getId()
        
        brains = self.portal_catalog({'portal_type': type,
                                        'getPrimaryAuthor': user_id,
                                        'sort_on':'created',
                                        'sort_order': 'reverse'})
        return [i.getObject() for i in brains]
                                                                                                                                                                        
    def get_addable_items_list(self):
        # TODO: this searches should be all in one place...
        #
        class Workaround:
            def portal_type(self):
                return self._portal_type
            def name(self):
                return self._name
            def __init__(self, _name, _portal_type):
                self._name = _name
                self._portal_type = _portal_type
        
        all_known = []
        all_known.append(Workaround('Conference Paper', 'ConferencePaper'))
        all_known.append(Workaround('Conference Event', 'ConferenceEvent'))
        all_known.append(Workaround('Article', 'Article'))
        return all_known


    def get_cfps(self):
        """
        This method returns all items of type 'type' for currently logged in user
        """
        ### WOrkaround
        brains = self.portal_catalog({'portal_type': ['Conference', 'Journal'],
                                        'sort_on':'created',
                                        'sort_order': 'reverse'})
        return [i.getObject() for i in brains]
                                                                                                                                                                        

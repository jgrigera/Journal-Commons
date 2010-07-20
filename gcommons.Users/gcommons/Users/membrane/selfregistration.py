
import logging
from OFS.SimpleItem import SimpleItem
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.membrane.interfaces import IUserAdder
from zope.interface import implements


logger = logging.getLogger("gcommons.Users.membrane.selfregistration")



class UserAdder(SimpleItem):
    """
    UserAdder utility that knows how to add SimpleMembers.
    """
    implements(IUserAdder)
    
    def addUser(self, login, password):
        """
        Adds a SimpleMember object at the root of the Plone site.
        """
        logger.info("Hello, userAdder!")
        portal = getToolByName(self, 'portal_url').getPortalObject()
        _createObjectByType('gcPerson', portal, login, password=password, userName=login)

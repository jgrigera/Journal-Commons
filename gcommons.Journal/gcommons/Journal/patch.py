
from Products.CMFCore.utils import _limitGrantedRoles
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.RegistrationTool import RegistrationTool


import logging
logger = logging.getLogger('gcommons.Journal')


# Monkey patched

def addMember(self, id, password, roles=('JournalAuthor',), domains='',
                  properties=None, REQUEST=None):
        '''Creates a PortalMember and returns it. The properties argument
        can be a mapping with additional member properties. Raises an
        exception if the given id already exists, the password does not
        comply with the policy in effect, or the authenticated user is not
        allowed to grant one of the roles listed (where Member is a special
        role that can always be granted); these conditions should be
        detected before the fact so that a cleaner message can be printed.
        '''
        logger.warning("Hola")
        # XXX: this method violates the rules for tools/utilities:
        # it depends on a non-utility tool
        if not self.isMemberIdAllowed(id):
            raise ValueError(_(u'The login name you selected is already in '
                               u'use or is not valid. Please choose another.'))

        failMessage = self.testPasswordValidity(password)
        if failMessage is not None:
            raise ValueError(failMessage)

        if properties is not None:
            failMessage = self.testPropertiesValidity(properties)
            if failMessage is not None:
                raise ValueError(failMessage)

        # Limit the granted roles.
        # Anyone is always allowed to grant the 'Member' role.
        logger.warning("hola 2 %s" % roles)
        _limitGrantedRoles(roles, self, ('Member','JournalAuthor',))
        logger.warning("hola 3")

        membership = getToolByName(self, 'portal_membership')
        membership.addMember(id, password, roles, domains, properties)

        member = membership.getMemberById(id)
        self.afterAdd(member, id, password, properties)
        return member




logger.warning('Monkey Patching Products.CMFDefault.RegisrationTool.addMember')
RegistrationTool._addMember = RegistrationTool.addMember
RegistrationTool.addMember = addMember

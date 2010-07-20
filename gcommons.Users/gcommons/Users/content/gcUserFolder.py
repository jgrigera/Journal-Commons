# -*- coding: utf-8 -*-
"""Definition of the gcUserFolder content type
"""

__docformat__ = 'plaintext'


# Zope
from zope.interface import implements, directlyProvides
from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent

# Plone
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.permissions import View, ManageUsers
from Products.CMFCore.utils import getToolByName

# Membrane
from Products.membrane.interfaces import IPropertiesProvider
from Products.membrane.utils import getFilteredValidRolesForPortal

# gcommons
from gcommons.Users import UsersMessageFactory as _
from gcommons.Users.interfaces import IgcUserFolder
from gcommons.Users.config import PROJECTNAME


gcUserFolderSchema = folder.ATBTreeFolderSchema.copy() + atapi.Schema((

))


def finalizeUserFolderSchema(Schema):
    Schema['title'].storage = atapi.AnnotationStorage()
    Schema['description'].storage = atapi.AnnotationStorage()

    schemata.finalizeATCTSchema(
        Schema,
        folderish=True,
        moveDiscussion=False
    )
    return Schema


class gcUserFolder(folder.ATBTreeFolder):
    """gcommons User Folder"""
    security = ClassSecurityInfo()
    implements(IgcUserFolder, IPropertiesProvider)

    meta_type = "gcUserFolder"
    schema = finalizeUserFolderSchema(gcUserFolderSchema)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # Methods
    security.declareProtected(View, 'getPeople')
    def getPeople(self):
        """Return a list of people contained within this FacultyStaffDirectory."""
        portal_catalog = getToolByName(self, 'portal_catalog')
        results = portal_catalog(path='/'.join(self.getPhysicalPath()), portal_type='FSDPerson', depth=1)
        return [brain.getObject() for brain in results]

    security.declareProtected(View, 'getSortedPeople')
    def getSortedPeople(self):
        """ Return a list of people, sorted by SortableName
        """
        people = self.getPeople()
        return sorted(people, cmp=lambda x,y: cmp(x.getSortableName(), y.getSortableName()))

    security.declarePrivate('getRoleSet')
    def getRoleSet(self):
        """Get the roles vocabulary to use."""
        portal_roles = getFilteredValidRolesForPortal(self)
        allowed_roles = [r for r in portal_roles if r not in INVALID_ROLES]
        return allowed_roles

    #
    # Validators
    #
    security.declarePrivate('validate_id')
    def validate_id(self, value):
        """Ensure the id is unique, also among groups globally."""
        if value != self.getId():
            parent = aq_parent(aq_inner(self))
            if value in parent.objectIds():
                return "An object with id '%s' already exists in this folder" % value
        
            groups = getToolByName(self, 'portal_groups')
            if groups.getGroupById(value) is not None:
                return "A group with id '%s' already exists in the portal" % value
                
atapi.registerType(gcUserFolder, PROJECTNAME)

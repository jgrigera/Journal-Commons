## Script (Python) "join_form"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=type_name=None
from Products.CMFCore.utils import getToolByName

portal = context.portal_url.getPortalObject() 
membership_tool = getToolByName(context, 'portal_membership')
membrane_tool = getToolByName(context, 'membrane_tool')

#
# No easy way of doing this cleanly. 
# We are now delivering a copy of Plone 3.x personalize_form as plone_... awfull.
# 
member = membership_tool.getAuthenticatedMember()
user = member.getUser()

try:
    foundUser = membrane_tool.searchResults(getUserName=user.getUserName())[0] # grab the first match
    realUser = foundUser.getObject()
    #context.portal_gcommons_users.me(realUser)
    url = "%s/portal_gcommons_users/%s/view" % (context.portal_url(),member.getId() )
except IndexError:
    # Probably not a Membrane Type
    url = "%s/plone_personalize_form" % context.portal_url()


context.REQUEST.RESPONSE.redirect(url)

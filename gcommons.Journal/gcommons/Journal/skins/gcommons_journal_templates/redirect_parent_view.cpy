## Controller Python Script "register"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=password='password', password_confirm='password_confirm', came_from_prefs=None
##title=Register a User
##
context.plone_utils.addPortalMessage(u'Draft added.')

#context.REQUEST.RESPONSE.redirect(context.aq_parent.absolute_url())

state.setNextAction('redirect_to:string:%s' % context.aq_parent.absolute_url())
return state

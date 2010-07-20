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
from Products.CMFPlone import PloneMessageFactory as _     
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import transaction_note
from ZODB.POSException import ConflictError
import logging
logger = logging.getLogger("gcommons.Users.skins.register")

portal = context.portal_url.getPortalObject()
portal_registration = getToolByName(context, 'portal_registration')
portal_memberdata = getToolByName(context, 'portal_memberdata')
gcommons_users = getToolByName(context, 'portal_gcommons_users')


REQUEST = context.REQUEST
username = REQUEST['username']
password = REQUEST.get('password') or portal_registration.generatePassword()


logger.info("Creating user %s" % username)
try:
	member = gcommons_users.addMember(username, password, properties=REQUEST, REQUEST=context.REQUEST)
except AttributeError,e:
	logger.info("Error %s" % str(e))
	state.setError('username', _(u'The login name you selected is already in use or is not valid. Please choose another.' ) )
	context.plone_utils.addPortalMessage(_(u'Please correct the indicated errors.'), 'error')
	return state.set(status='failure')


transactionnote = 'Initiated creation of %s with id %s in %s' % (member.getTypeInfo().getId(), member.getId(), member.absolute_url())
logger.info(transactionnote)
transaction_note(transactionnote)


if portal.validate_email:
    try:
		portal_registration.registeredNotify(username)
    except ConflictError:
        raise
    except Exception, err:

        # TODO registerdNotify calls into various levels.  Lets catch all
        # exceptions.  Should not fail.  They cant CHANGE their password ;-)
        # We should notify them.
        #
        # (MSL 12/28/03) We also need to delete the just made member and return to the join_form.
		logger.info("Except %s" % str(err))
		state.set(came_from='login_success')
		
		if portal.validate_email:
			context.acl_users.userFolderDelUsers([username,], REQUEST=context.REQUEST)
			msg = _(u'status_fatal_password_mail',
				default=u'Failed to create your account: we were unable to send your password to your email address: ${address}',
				mapping={u'address' : str(err)})
			context.plone_utils.addPortalMessage(msg, 'error')
			return state.set(status='failure')
		else:
			msg = _(u'status_nonfatal_password_mail',
			        default=u'You account has been created, but we were unable to send your password to your email address: ${address}',
			        mapping={u'address' : str(err)})
			context.plone_utils.addPortalMessage(msg, 'error')

state.set(came_from=REQUEST.get('came_from','login_success'))

if came_from_prefs:
    context.plone_utils.addPortalMessage(_(u'User added.'))
    state.set(status='prefs')

transaction_note('%s registered' % username)
logger.info('%s registered' % username)

return state

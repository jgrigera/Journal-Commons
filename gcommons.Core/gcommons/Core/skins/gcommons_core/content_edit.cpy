## Script (Python) "content_edit"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id=''
##

#Save changes normal way
state = context.content_edit_impl(state, id)

# if this is edit_and_publish
if context.REQUEST.get('form.button.edit_and_publish'):

    from Products.Archetypes.utils import addStatusMessage
    from Products.CMFCore.utils import getToolByName

    addStatusMessage(context.REQUEST,"Submitted to Editorial Board")
    context = state.getContext()
    #change workflow
    portal_workflow = getToolByName(context, 'portal_workflow', None)
    if portal_workflow.getInfoFor(context, 'review_state') != 'eb_draft':
        try:
            portal_workflow.doActionFor(context, 'submittoeb')
            msg = u"Changes saved and document published."
        except:
            msg = u"Changes saved but document not published."
            context.plone_utils.addPortalMessage(msg)

            
return state


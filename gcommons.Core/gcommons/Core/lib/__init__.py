

from Products.CMFCore.utils import getToolByName


def is_gcommons_Users_installed(context):
    portal_quickinstaller = getToolByName(context, 'portal_quickinstaller')
    return portal_quickinstaller.isProductInstalled('gcommons.Users')

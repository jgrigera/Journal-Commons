

from StringIO import StringIO
from Products.CMFCore.utils import getToolByName


import logging
logger = logging.getLogger("Uninstall")

def beforeUninstall(self, reinstall, product, cascade):
    """ try to call a custom beforeUninstall method in 'AppInstall.py'
        method 'beforeUninstall'
    """
    
    logger.info("Problem: Uninstalling gcommons.Users but leaving stuff behind!")
    
    # Cascade contains the items that should be removed
    # keep types, workflows and portalobjects (i.e. tool)
    for item in ('types', 'portalobjects', 'workflows'):
	if item in cascade:
	    cascade.remove(item)

    out = StringIO()
    print >>out, 'gcommons.Users beforeUninstall:'
    print >>out, 'I will prevent types and tools from being deleted'
    print >>out, 'This needs a better approach, but all your users would be lost!'
    
    return (out, cascade)




from StringIO import StringIO
import transaction
from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from zExceptions import NotFound

from Products.CMFQuickInstallerTool.QuickInstallerTool import AlreadyInstalled

from Products.Poi.config import PROJECTNAME

import logging
logger = logging.getLogger("Uninstall")

def beforeUninstall(self, reinstall, product, cascade):
    """ try to call a custom beforeUninstall method in 'AppInstall.py'
        method 'beforeUninstall'
    """
    out = StringIO()
    
    logger.info("Problem: Uninstalling gCommons.Users but leaving stuff behind!")
    
    # Cascade contains the items that should be removed
    # keep types, workflows and portalobjects (i.e. tool)
    for item in ('types', 'portalobjects', 'workflows'):
	cascade.remove(item)

    print >>out, 'gcommons.Users beforeUninstall:'
    print >>out, 'I will prevent types and tools from being deleted'
    print >>out, 'This needs a better approach, but all your users would be lost!'
    
    return (out, cascade)


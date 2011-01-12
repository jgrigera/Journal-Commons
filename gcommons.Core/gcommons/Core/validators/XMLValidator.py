

from ZPublisher.HTTPRequest import FileUpload

# XML
# rename to allow other implementations in the future 
from xml.dom.minidom import parseString as XMLParseString
from xml.parsers.expat import ExpatError as XMLError

# Validator
from zope.interface import implements
from Products.validation.interfaces import ivalidator

try: 
     # Plone 4 and higher 
     import plone.app.upgrade 
     USE_ZOPE2_VALIDATORS = False 
except ImportError: 
     # BBB Plone 3 
     USE_ZOPE2_VALIDATORS = True 


import logging
logger = logging.getLogger('gcommons.Core.validators.XMLValidator')

#
# Validators
class XMLValidator:
    if USE_ZOPE2_VALIDATORS:
        __implements__ = (ivalidator,)
    else:
        implements(ivalidator,)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        """
        compile value and return any errors in XML
        """
        if isinstance(value, FileUpload) or isinstance(value, file):
            string = value.read()
            name = value.filename
        else:
            string = value
            name = '(edit)'

        try:
            parsed = XMLParseString(string)
        except XMLError, e:
            logging.info("Error in %s: %s" % (name, str(e)))
            return "Error parsing XML in %s: %s" % (name, str(e))



from ZPublisher.HTTPRequest import FileUpload

# XML
# rename to allow other implementations in the future 
from xml.dom.minidom import parseString as XMLParseString
from xml.parsers.expat import ExpatError as XMLError

# Validator
from Products.validation.interfaces import ivalidator


import logging
logger = logging.getLogger('gcommons.Core.validators.XMLValidator')

#
# Validators
class XMLValidator:
    __implements__ = (ivalidator,)

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

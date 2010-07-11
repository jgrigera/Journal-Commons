

from Products.validation.config import validation

from XMLValidator import XMLValidator

validation.register(XMLValidator('isValidXML'))

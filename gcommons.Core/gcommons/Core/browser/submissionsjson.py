# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.navigation.root import getNavigationRoot
from Products.Five import BrowserView
from logging import getLogger
from plone.app.content.utils import json_dumps
from plone.app.content.utils import json_loads
from plone.app.querystring import queryparser
from plone.app.widgets.interfaces import IFieldPermissionChecker
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.supermodel.utils import mergedTaggedValueDict
from types import FunctionType
from zope.component import getUtility
from zope.component import queryAdapter
from zope.component import queryUtility
from zope.schema.interfaces import ICollection
from zope.schema.interfaces import IVocabularyFactory
from zope.security.interfaces import IPermission
from Products.CMFPlone import PloneMessageFactory as _
from zope.i18n import translate
from Products.CMFPlone.utils import safe_unicode
import inspect
import itertools

logger = getLogger(__name__)

MAX_BATCH_SIZE = 500  # prevent overloading server



class SubmissionsJsonView(BrowserView):

    def __call__(self):
        """
        Accepts GET parameters of:
        name: Name of the vocabulary
        field: Name of the field the vocabulary is being retrieved for
        query: string or json object of criteria and options.
            json value consists of a structure:
                {
                    criteria: object,
                    sort_on: index,
                    sort_order: (asc|reversed)
                }
        attributes: comma seperated, or json object list
        batch: {
            page: 1-based page of results,
            size: size of paged results
        }
        """
        context = self.context
        self.request.response.setHeader("Content-type", "application/json")
	Fields = [ 
	    { 'title': 'Title',           'value': 'title' },
	    { 'title': 'Abstract',        'value': 'description' },
	    { 'title': 'Requirements',    'value': 'specialRequirements' },
	    { 'title': 'Keywords',        'value': 'subject' },
	]
	
	results = []
	for item in context.searchSubmissions():
	    row = {}
	    obj = item.getObject()
	    for field in Fields:
		try:
		    schemafield = obj.Schema().getField( field['value'] )
		    if schemafield is None:
			logger.info("Wrong field %s in item type %s" % (field['value'], item.portal_type))
			continue
		    
		    value = schemafield.getAccessor(obj)()
		    if value is not None:
			row[field['title']] = value.decode('utf-8','ignore')
		except UnicodeDecodeError:
		    row[field['column']] = "UNICODE ERROR!!"
		
	    row['Authors'] = obj.getRelators()
	    row['State'] = obj.get_review_state()
	    results.append(row)
	
	return json_dumps({'items':results})


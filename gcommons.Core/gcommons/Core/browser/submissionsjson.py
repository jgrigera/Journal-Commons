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
	    { 'title': 'Author',          'value': 'primaryAuthor' },
	    { 'title': 'Authors',         'value': 'unconfirmedExtraAuthors' },
	    { 'title': 'Title',           'value': 'title' },
	    { 'title': 'Abstract',        'value': 'description' },
	    { 'title': 'Requirements',    'value': 'specialRequirements' },
	    { 'title': 'Keywords',        'value': 'description' },
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
		
	    row['State'] = obj.get_review_state()
	    results.append(row)
	
	return json_dumps({'items':results})

        try:
            vocabulary = self.get_vocabulary()
        except VocabLookupException, e:
            return json_dumps({'error': e.message})

        results_are_brains = False
        if hasattr(vocabulary, 'search_catalog'):
            query = self.parsed_query()
            results = vocabulary.search_catalog(query)
            results_are_brains = True
        elif hasattr(vocabulary, 'search'):
            try:
                query = self.parsed_query()['SearchableText']['query']
            except KeyError:
                results = iter(vocabulary)
            else:
                results = vocabulary.search(query)
        else:
            results = vocabulary

        try:
            total = len(results)
        except TypeError:
            # do not error if object does not support __len__
            # we'll check again later if we can figure some size
            # out
            total = 0

        # get batch
        batch = _parseJSON(self.request.get('batch', ''))
        if batch and ('size' not in batch or 'page' not in batch):
            batch = None  # batching not providing correct options
        if batch:
            # must be slicable for batching support
            page = int(batch['page'])
            size = int(batch['size'])
            if size > MAX_BATCH_SIZE:
                raise Exception('Max batch size is 500')
            # page is being passed in is 1-based
            start = (max(page - 1, 0)) * size
            end = start + size
            # Try __getitem__-based slice, then iterator slice.
            # The iterator slice has to consume the iterator through
            # to the desired slice, but that shouldn't be the end
            # of the world because at some point the user will hopefully
            # give up scrolling and search instead.
            try:
                results = results[start:end]
            except TypeError:
                results = itertools.islice(results, start, end)

        # build result items
        items = []

        attributes = _parseJSON(self.request.get('attributes', ''))
        if isinstance(attributes, basestring) and attributes:
            attributes = attributes.split(',')

        translate_ignored = [
            'Creator', 'Date', 'Description', 'Title', 'author_name',
            'cmf_uid', 'commentators', 'created', 'effective', 'end',
            'expires', 'getIcon', 'getId', 'getRemoteUrl', 'in_response_to',
            'listCreators', 'location', 'modified', 'start', 'sync_uid',
            'path', 'getURL', 'EffectiveDate', 'getObjSize', 'id',
            'UID', 'ExpirationDate', 'ModificationDate', 'CreationDate',
        ]
        if attributes:
            base_path = getNavigationRoot(context)
            for vocab_item in results:
                if not results_are_brains:
                    vocab_item = vocab_item.value
                item = {}
                for attr in attributes:
                    key = attr
                    if ':' in attr:
                        key, attr = attr.split(':', 1)
                    if attr in _unsafe_metadata:
                        continue
                    if key == 'path':
                        attr = 'getPath'
                    val = getattr(vocab_item, attr, None)
                    if callable(val):
                        if attr in _safe_callable_metadata:
                            val = val()
                        else:
                            continue
                    if key == 'path':
                        val = val[len(base_path):]
                    if key not in translate_ignored and isinstance(val, basestring):
                        item[key] = translate(_(safe_unicode(val)), context=self.request)
                    else:
                        item[key] = val
                items.append(item)
        else:
            for item in results:
                items.append({'id': item.value, 'text': item.title})

        if total == 0:
            total = len(items)

        return json_dumps({
            'results': items,
            'total': total
        })

    def parsed_query(self, ):
        query = _parseJSON(self.request.get('query', ''))
        if isinstance(query, basestring):
            query = {'SearchableText': {'query': query}}
        elif query:
            parsed = queryparser.parseFormquery(
                self.get_context(), query['criteria'])
            if 'sort_on' in query:
                parsed['sort_on'] = query['sort_on']
            if 'sort_order' in query:
                parsed['sort_order'] = str(query['sort_order'])
            query = parsed
        else:
            query = {}
        return query



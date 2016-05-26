# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone.app.content.utils import json_dumps
from logging import getLogger
import hashlib


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
	    { 'title': 'Requirements',    'value': 'specialRequirements' },
	    { 'title': 'Keywords',        'value': 'subject' },
	]
	
	results = []
	for item in context.searchSubmissions():
	    row = {}
	    obj = item.getObject()
	    row['id'] = obj.UID()
	    row['label'] = obj.Title()
            row['Title'] = obj.Title()
	    row['Authors'] = obj.getRelators_text(brief=True)
            row['Keywords'] = obj.Subject()
	    row['State'] = obj.get_review_state()
	    row['url'] = obj.absolute_url()
	    row['type'] = obj.portal_type
	    row['SubType'] = obj.get_item_subtype()

            abstract = obj.Description()
            abstracted = {}
            abstracted['id'] = hashlib.md5(abstract).hexdigest()
            abstracted['label'] = abstract
            abstracted['type'] = 'Details'
	    abstracted['short'] = 'More details...'
            abstracted['url'] = obj.absolute_url()
            row['Abstract'] = abstracted['id']
	    results.append(row)

            results.append(abstracted)
            
	return json_dumps(
	    {'items' : results,
             'properties' :  [{ 'Abstract': 'item' }],
	     'types': [{ 'ConferencePaper': {'pluralLabel': 'Papers',} },
		       { 'Details' :  {'pluralLabel': 'Papers',}  }],
	    }
        )


import os, logging, urllib2, exceptions, sys
import simplejson as json

logger = logging.getLogger('journalcommons.Utils.gcommonsWorldcat')

class IsbnError (exceptions.ValueError):
    def __init__ (self, msg):
	exceptions.ValueError.__init__ (self, msg)

class NetworkError (exceptions.ValueError):
    def __init__ (self, msg):
	exceptions.ValueError.__init__ (self, msg)
		
class gcommonsWorldcat:
    def __init__(self, isbn=None,host='xisbn.worldcat.org'):
        try:
	    self._data = self._get_worldcat_byISBN_json(isbn,host)
	except (NetworkError), e:
            raise
        self._status = self._data['stat']
        if self._status == 'ok':
	    self._book = self._data['list'][0]
	    self._title = self._book['title']
	    self._year = self._book['year']
	    self._author = self._book['author']
	    self._publisher = self._book['publisher']
	    self._city = self._book['city']
	    self._language = self._book['lang']
	    self._edition = self._book['ed']
	    self._url = self._book['url']
	elif self._status == 'invalidId':
            message = "Worldcat invalid isbn: %s " % isbn
	    logger.error("%s" % message)
	    raise IsbnError, message
    def title(self):
	return self._title
    def year(self):
	return self._year
    def author(self):
	return self._author
    def publisher(self):
	return self._publisher
    def city(self):
	return self._city
    def language(self):
	return self._language
    def edition(self):
	return self._edition
    def url(self):
	return self._url
    def book(self):
	return self._book
    def data(self):
	return self._data
    def status(self):
	return self._status

    def _get_worldcat_byISBN_json (self, isbn, domain):
	url="http://" + domain + "/webservices/xid/isbn/" + isbn + "?method=getMetadata&format=json&fl=*"
	try:
	    content = self._get_from_url(url)
            logger.info("Feteched bookd metadata from %s" % url)
	    return json.loads(content)
	except (NetworkError), e:
	    logger.error("%s" % e)
	    raise

    def _get_from_url (self, url):
	req = urllib2.Request(url)
	try:
	    res = urllib2.urlopen(req)
	    return res.read()
	except IOError, e:
	    if hasattr(e, 'reason'):
		raise NetworkError, "Sever not reachable %s, URL=%s" % (e.reason, url)
	    elif hasattr(e, 'code'):
		raise NetworkError, "Server returned error code: %s, URL=%s" % (e.code, url)
	    return None

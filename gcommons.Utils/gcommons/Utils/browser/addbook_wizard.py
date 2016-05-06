
import logging
from zope import interface, schema
from zope.interface import implements                                                                                                                                                   
from z3c.form import form, field, button, widget
from plone.z3cform.layout import FormWrapper, wrap_form
from z3c.form import subform

# Do not mix with Products.Five.browser.pagetemplatefile.ViewPageTemplateFile
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile as Zope3PageTemplateFile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as FiveViewPageTemplateFile
                                                                                                                                                                                              
# z3c.form Choice
from zope.schema.interfaces import IContextSourceBinder
from z3c.formwidget.query.interfaces import IQuerySource                                                                                                                                
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


# Json
try:
    import json
except ImportError:    
    # Python 2.4 needs simplejson
    import simplejson as json

logger = logging.getLogger('gcommons.Utils.browser.FillBookDetails')

try:
    from gcommons.Utils.lib.worldcat import gcommonsWorldcat, IsbnError, NetworkError
except ImportError:
    pass

class BookSources(object):
    implements(IQuerySource)
    vocabulary = SimpleVocabulary((SimpleTerm(u'worldcat', 'WorldCat', u'WorldCat '),))

    def __init__(self, context):
        self.context = context

    __contains__ = vocabulary.__contains__
    __iter__ = vocabulary.__iter__
    getTerm = vocabulary.getTerm
    getTermByToken = vocabulary.getTermByToken

    def search(self, query_string):
        return [v for v in self if query_string.lower() in v.value.lower()]


class BookSourceBinder(object):
    implements(IContextSourceBinder)
    def __call__(self, context):
        return BookSources(context)  



class IFillBookDetails(interface.Interface):
    isbn = schema.TextLine(title=u"ISBN")
    book_sources = schema.Choice(title=u'Service',
        description=u'Which service to search.',
        source=BookSourceBinder(),
        required=True)    

#
# retrieve default ISBN value from isbn= if it is there in the request 
def defaultISBN(value):
    return value.request.get('isbn')

DefaultISBN = widget.ComputedWidgetAttribute(defaultISBN, field=IFillBookDetails['isbn'])                                                                                                                                        


class FillBookDetailsForm(form.Form):
    fields = field.Fields(IFillBookDetails)
    ignoreContext = True # don't use context to get widget data
    label = u"Search book"
    cancel = button.Button(title=u'Cancel')

    @button.buttonAndHandler(u'Search')
    def handleApply(self, action):
        pass
    

class FillBookDetailsView(FormWrapper):
    """ Render Plone frame around our form with little modifications """
    form = FillBookDetailsForm
    index = FiveViewPageTemplateFile("templates/addbook_wizard.pt")

    def __init__(self, context, request):
        # We can optionally set some variables in the constructor
        FormWrapper.__init__(self, context, request)
        self.isbn = self.request.get('isbn')
        logger.info( "REQUEST=%s" % self.isbn )

    def getList(self):
        """ Return how many books are availabe with this data """
        data, errors = self.form_instance.extractData()
        if data.has_key('isbn'):
            return self.searchIsbn(data['isbn'])
        return None
    
    def searchIsbn(self, isbn):
        try:
            worldcat = gcommonsWorldcat(isbn=isbn)
            return [worldcat.getAsMap()]
        except IsbnError:
            return None
        except NetworkError, e:
            return None

    # @json A decorator would be nice to have        
    def getAsJson(self, book):
        logger.info("book:%s" % book)
        return json.dumps ( book )

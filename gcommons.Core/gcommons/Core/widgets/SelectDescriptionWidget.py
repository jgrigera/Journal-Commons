

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.utils import mapply  
from Products.Five import BrowserView
import simplejson

class SelectDescriptionWidget(SelectionWidget):
    # Vocabulary= function should return extra descriptions when
    # called with 'extended=True'
    security = ClassSecurityInfo()

    _properties = SelectionWidget._properties.copy()
    _properties.update({
        'macro': 'selectdescription',
        'format': 'select',
        })


registerWidget(SelectDescriptionWidget,
               title='Select with Description',
               description="Select field which uses javascript to control an extended descriptin.",
               used_for=('Products.Archetypes.public.StringField',
                         'Products.Archetypes.Field.LinesField')
               )

# Javascript
JQUERY_ONLOAD = '''\
(function($) { $(function() {
%s
});})(jQuery);
'''
class ManageDescription(BrowserView):
     
    def __call__(self, field, context):
        """render javascript"""            
        return JQUERY_ONLOAD % self.renderJS(field, context)

    def renderJS(self, field, context):
        values = {}
        values['name'] = field.getName()
        values['array'] = self.getArrayJS(field, context)
        # maybe use AJAX: jq.getJSON('%(absolute_url)s/@@masterselect-jsonvalue', function(json) { 
        return """
jq('#%(name)s').change(function() {
            var sel = jq("#%(name)s").val();
            var values = %(array)s;
            var text = values[sel];
            jq("#%(name)s-selectdescription").html(text);
        });
""" % values
    
    def getArrayJS(self, field, context): 
        method = getattr(context, field.vocabulary, None)                                                                                                                  
        if method and callable(method):
            args = []                                                                                                                                                        
            kw = { 'content_instance' : context,                                                                                                                         
                    'field' : self,
                    'extended': True 
            }                                                                                                                                            
            value = mapply(method, *args, **kw)           
        return simplejson.dumps ( value )
    #( ["'%s':'%s'" % (k,v) for k,v in value.iteritems()] )





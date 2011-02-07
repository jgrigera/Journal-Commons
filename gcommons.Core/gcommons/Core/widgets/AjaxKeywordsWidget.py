"""

    Based on collective.ajaxkeywords, but for Archetypes, without grok dependency
"""
import logging
import copy
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from AccessControl import getSecurityManager
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.utils import mapply  
from Products.Five import BrowserView
try:
    import json
except ImportError:	
    # Python 2.4 needs simplejson
    import simplejson as json

logger = logging.getLogger("gcommons.Core.widgets.AjaxKeywordsWidget")



class AjaxKeywordsWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'format': "select", # possible values: select, checkbox
        'macro' : "ajaxkeywords",
        'size'  : 5,
        'vocab_source' : 'portal_catalog',
        'roleBasedAdd' : True,
        })

    security = ClassSecurityInfo()

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        """We need to get temporary values and assing here"""
        fieldName = field.getName()

        try:
            value = copy.copy(field._v_kwdajaxTmp)
            # it would be nice to cleanup as below, but cant understand why process_form is called many times during processForm
            #field._v_kwdajaxTmp = None
            if value is None:
                return empty_marker
            else:
                return value, {}
        except AttributeError:
            return empty_marker

registerWidget(AjaxKeywordsWidget,
               title='Ajax Keywords',
               description="Select field which uses javascript to control an extended descriptin.",
               used_for=('Products.Archetypes.Field.LinesField')
               )

# Javascript
JQUERY_ONLOAD = '''\
(function($) { $(function() {
%s
});})(jQuery);
'''
class ManageAjax(BrowserView):
     
    def __call__(self, field, context):
        """render javascript"""            
        return JQUERY_ONLOAD % self.renderJS(field, context)

    def renderJS(self, field, context):
        values = {}
        values['name'] = field.getName()
        values['availableTags'] = self.getAvailableTags(field, context)
        values['assignedTags'] = self.getAssignedTags(field, context)
        values['updateURL'] = "%s/widget_ajaxkeywords_update" % self.context.virtual_url_path()

#        if(getSecurityManager().checkPermission(permissions.ModifyPortalContent, self.context)): #No! should be the permission to manage keywords...
        values['allowAdd'] = 'true'
#        else:
#            allowEdit = 'false'

        return """
           $('#ajaxkeywords').tagHandler({
                availableTags: %(availableTags)s,
                updateURL: '%(updateURL)s',
                assignedTags: %(assignedTags)s,
                updateData: { fieldName: '%(name)s' },
                autocomplete: true,
                autoUpdate: true,
                delimiter: ';',
                allowEdit: true,
                allowAdd: %(allowAdd)s,
                minChars: 2,
            });""" % values
            
    def getAvailableTags(self, field, context):
        available_keywords = sorted(getToolByName(self.context, 'portal_catalog').uniqueValuesFor('Subject'))
        return json.dumps(available_keywords)
        
    def getAssignedTags(self, field, context):
        selected_keywords = sorted(self.context.Subject())
        return json.dumps(selected_keywords)
        

class UpdateAjax(BrowserView):
    """Save (temporarily) tags for future update
       CAVEAT/BUG: No way to edit an object simultaneously! Awfull results, probably...
    """
    def __call__(self):
        logger.info("Yahoo! %s = %s" % (self.request.get('fieldName'), self.request.get('tags[]')))
        logger.info("x %s" % self.context.virtual_url_path())
        fieldName = self.request.get('fieldName')
        if fieldName is None:
            return "Bad Request"
        
        field = self.context.getField(fieldName)
        try: 
            if field._v_kwdajaxTmp is None:
                 field._v_kwdajaxTmp = []
        except AttributeError:
            field._v_kwdajaxTmp = []
        
        field._v_kwdajaxTmp = self.request.get('tags[]')
        return ""

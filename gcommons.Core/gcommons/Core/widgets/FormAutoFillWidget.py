"""


  Form can be as you wish, but
    1. Use class="close" to cancel the form
    2. CAVEAT: We need at least one element to be the 'real' close, use e.g.
          <a href="#" class="close" style="visibility:hidden" />
    3. Use ids in the form id="return_xxx" for items that should return values
   


"""

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import StringWidget
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Registry import registerPropertyType

class FormAutoFillWidget(StringWidget):
    # Vocabulary= function should return extra descriptions when
    # called with 'extended=True'
    security = ClassSecurityInfo()

    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro': 'formautofill',
        'helper_url': None,
        'helper_text': 'Open Subform',
        'icon':  'autofill.png'
        })
    

registerPropertyType('helper_url', 'string', FormAutoFillWidget)
registerPropertyType('helper_text', 'string', FormAutoFillWidget)
registerPropertyType('icon', 'string', FormAutoFillWidget)     

registerWidget(FormAutoFillWidget,
               title='Form Auto Fill',
               description="A string field which uses javascript to fill the rest of the form.",
               used_for=('Products.Archetypes.public.StringField',
                         'Products.Archetypes.Field.LinesField')
               )


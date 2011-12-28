"""Definition of the SubmissionsFolder content type
"""

import logging
from cStringIO import StringIO
from zope.interface import implements, directlyProvides

from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ModifyPortalContent, View
from Products.CMFCore.utils import getToolByName

# Archetypes
from Products.Archetypes import atapi
from plone.app.folder import folder
from Products.ATContentTypes.content import schemata

# gcommons
from gcommons.Core import CoreMessageFactory as _
from gcommons.Core.interfaces import ISubmissionsFolder
from gcommons.Core.config import PROJECTNAME

from plone.portlets.interfaces import IPortletManager
from plone.portlets.constants import USER_CATEGORY
from plone.app.portlets.interfaces import IDefaultDashboard
from plone.app.portlets import portlets

logger = logging.getLogger('gcommons.Core.content.SubmissionsFolder')



SubmissionsFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.TextField(
        name='helpTextAnon',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword'),
        widget=atapi.RichWidget(
            label="Anonymous Help text",
            description="Enter any introductory help text you'd like to display for users that have not yet logged in.",
            label_msgid='gcommons_label_helpTextAnon',
            description_msgid='gcommons_help_helpTextAnon',
            i18n_domain='gcommons.Core',
        ),
        default="""
      <h2>Welcome to the registration and paper submission system</h2>
        <p>
        To register or submit your piece, follow these steps:</p>
        <dl><dt>1. Create account (if you dont have one)</dt>
        Click on "Create account" and fill out the form. An account will be created and an e-mail is sent to you for confirmation.</dl>
        <dl><dt>2. Login </dt>        You may log in right after receiving an email by using the "Login" link.</dl>
        <dl><dt>3. Submit your abstract </dt></dl>
        <dl><dt>4. Finish editing and send to editors</dt>    Click on "Submit to Editors"</dl>
        You are done! Thanks for submitting the product of your research.
         
        """,
        default_output_type='text/html',
        searchable=True
    ),

    atapi.TextField(
        name='helpText',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword'),
        widget=atapi.RichWidget(
            label="Help text",
            description="Enter any introductory help text you'd like to display on the tracker front page.",
            label_msgid='gcommons_label_helpText',
            description_msgid='gcommons_help_helpText',
            i18n_domain='gcommons.Core',
        ),
        default_output_type='text/html',
        searchable=True,
        default="""
        <h2>Welcome to the registration and paper submission system</h2>

        You are a registered user. To submit a paper:

        <dl><dt>Submit your abstract </dt>
            Click on 'Submit conference paper' below and fill in the details
        </dl>
        <dl><dt>Revise your paper and submit</dt>
                You can edit the submission later, when finished editing click on 'Submit to Editors'
        </dl>

        To submit a panel or session:
        <dl>
            <dt>Submit your panel proposal</dt>
                Click on 'Submit conference event' below and fill in the details. 
        </dl>
        <dl><dt>Revise your proposed panel or event and submit</dt>
                You can edit the submission later, when all required conditions are met, you can click on 'Submit to Editors'
        </dl>

        
        Then you will be done! Thanks for submitting the product of your work.
        """,
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

SubmissionsFolderSchema['title'].storage = atapi.AnnotationStorage()
SubmissionsFolderSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(
    SubmissionsFolderSchema,
    folderish=True,
    moveDiscussion=False
)


class SubmissionsFolder(folder.ATFolder):
    """Large folder to hold all pending gcommons Submissions"""
    implements(ISubmissionsFolder)

    meta_type = "SubmissionsFolder"
    schema = SubmissionsFolderSchema
    security  = ClassSecurityInfo()

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    helptext = atapi.ATFieldProperty('helpText')
    helptextanon  = atapi.ATFieldProperty('helpTextAnon')

    # Plone 4 compatibility with BaseBTree
    _ordering = 'unordered'     # old large folder remain unordered at first 
    
    # Helpers
    def getSubmittablePortalTypes(self):
        # Acquire config from container
        config = self.aq_getConfig()
        return [item.portal_type() for item in config.getSubmittableItems()]

    def searchSubmissions(self, portal_type=None, state=None, **kw):
        # maybe...
        #brains = self.context.listFolderContents(contentFilter={"portal_type" : "Article"})
        criteria = {
            'sort_on':'created',
            'sort_order': 'reverse',
            'path': '/'.join(self.getPhysicalPath())
        }
        if portal_type is not None:
            criteria['portal_type'] = portal_type
        else:
            criteria['portal_type'] = self.getSubmittablePortalTypes()

        if state is not None:
            criteria['review_state'] = state
            
        for item in kw.keys():
            if kw[item] is not None:
                criteria[item] = kw[item]
        
        return self.portal_catalog(criteria)


    security.declareProtected(View, 'download_all_as_excel')
    def download_all_as_excel(self, **kwargs):
	"""
        
	"""
	data = StringIO()

	try:
	    import pyExcelerator as xls
	except ImportError:
	    data.write("Sorry, low level error, no pyExcelerator. Cant generate XLSs.")
	    data.seek(0)
	    return data
        
        # Open Excel
	wb = xls.Workbook()
	ws0 = wb.add_sheet('Abstracts')
	
	Fields = [ 
	    { 'column': 0, 'title': 'Author',          'value': 'primaryAuthor' },
	    { 'column': 1, 'title': 'Authors',         'value': 'unconfirmedExtraAuthors' },
	    { 'column': 2, 'title': 'Title',           'value': 'title' },
	    { 'column': 3, 'title': 'Abstract',        'value': 'description' },
	    { 'column': 4, 'title': 'Requirements',    'value': 'specialRequirements' },
#	    { 'column': 3, 'title': 'Part of Panel?',  'value': 'isPartPanel' },
	]
	
	# Cell Style
	style = xls.Style.XFStyle()
	style.alignment.wrap = xls.Formatting.Alignment.WRAP_AT_RIGHT
	style.alignment.vert = xls.Formatting.Alignment.VERT_TOP

	# Header
	for field in Fields:
	    ws0.write(0, field['column'], field['title'])

	n=0
	for item in self.searchSubmissions():
	    n = n + 1
	    for field in Fields:
		try:
		    obj = item.getObject()
		    schemafield = obj.Schema().getField( field['value'] )
		    if schemafield is None:
			logger.info("Wrong field %s in item type %s" % (field['value'], item.portal_type))
			continue
		    
		    value = schemafield.getAccessor(obj)()
		    if value is not None:
			ws0.write(n, field['column'], value.decode('utf-8','ignore'), style)
		except UnicodeDecodeError:
		    ws0.write(n,field['column'], "UNICODE ERROR!!")
	
	wb.save(data)
	data.seek(0)
	return data


atapi.registerType(SubmissionsFolder, PROJECTNAME)

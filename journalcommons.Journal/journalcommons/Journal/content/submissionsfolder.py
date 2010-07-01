"""Definition of the SubmissionsFolder content type
"""

from zope.interface import implements, directlyProvides

from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

from journalcommons.Journal import JournalMessageFactory as _
from journalcommons.Journal.interfaces import ISubmissionsFolder
from journalcommons.Journal.config import PROJECTNAME

from plone.portlets.interfaces import IPortletManager
from plone.portlets.constants import USER_CATEGORY
from plone.app.portlets.interfaces import IDefaultDashboard
from plone.app.portlets import portlets

#TODO: move this to jcommons

SubmissionsFolderSchema = folder.ATBTreeFolderSchema.copy() + atapi.Schema((

    # -*- Your Archetypes field definitions here ... -*-
    atapi.TextField(
        name='helpTextAnon',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',
                                 'application/msword'),
        widget=atapi.RichWidget(
            label="Anonymous Help text",
            description="Enter any introductory help text you'd like to display for users that have not yet logged in.",
            label_msgid='jcommons_label_helpTextAnon',
            description_msgid='jcommons_help_helpTextAnon',
            i18n_domain='journalcommons.Journal',
        ),
        default="""
      <h2>Welcome to the registration and paper submission system</h2>
        <p>
        To register or submit your piece, follow these steps:</p>
        <dl><dt>1. Create account</dt>
        Click on "Create account" and fill out the form. An account will be created and an e-mail is sent to you for confirmation.</dl>
        <dl><dt>2. Login </dt>
        You may log in right after receiving an email by using the "Login" link.</dl>
        <dl><dt>3. Submit your abstract </dt></dl>
        <dl><dt>4. Finish editing and send to editors</dt>
        Click on "Submit to Editors"</dl>
        You are done! Thanks for submitting the product of your work.
         
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
            label_msgid='jcommons_label_helpText',
            description_msgid='jcommons_help_helpText',
            i18n_domain='journalcommons.Journal',
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

#    BooleanField(
#        name='sendNotificationEmails',
#        default=True,
#        widget=BooleanWidget(
#            label="Send notification emails",
#            description="If selected, tracker managers will receive an email each time a new issue or response is posted, and issue submitters will receive an email when there is a new response and when an issue has been resolved, awaiting confirmation.",
#            label_msgid='Poi_label_sendNotificationEmails',
#            description_msgid='Poi_help_sendNotificationEmails',
#            i18n_domain='Poi',
#        )
#    ),

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


class SubmissionsFolder(folder.ATBTreeFolder):
    """Large folder to hold all pending Journal Submissions"""
    implements(ISubmissionsFolder)

    meta_type = "SubmissionsFolder"
    schema = SubmissionsFolderSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    # -*- Your ATSchema to Python Property Bridges Here ... -*-
    helptext = atapi.ATFieldProperty('helpText')
    helptextanon  = atapi.ATFieldProperty('helpTextAnon')
    
    
atapi.registerType(SubmissionsFolder, PROJECTNAME)

# -*- coding: utf-8 -*-
"""Definition of the gcPerson content type
"""
__docformat__ = 'plaintext'

import logging
import re
from sha import sha
from DateTime import DateTime
from cStringIO import StringIO

# zope
from zope.event import notify
from zope.interface import implements, directlyProvides, classImplements
from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent

# Plone
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.CMFCore.permissions import View, ModifyPortalContent, SetOwnPassword, SetOwnProperties
from Products.CMFCore.utils import getToolByName

# membrane
from Products.membrane.interfaces import IUserAuthProvider, IPropertiesProvider, IGroupsProvider, IGroupAwareRolesProvider, IUserChanger


from zope.app.annotation.interfaces import IAttributeAnnotatable, IAnnotations
from Products.ATContentTypes.lib.calendarsupport import n2rn, foldLine
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFPlone.CatalogTool import getObjPositionInParent
from Products.CMFPlone.utils import safe_unicode
from Products.validation import validation


# gcommons
from gcommons.Users import UsersMessageFactory as _
from gcommons.Users.interfaces import IgcPerson
from gcommons.Users.interfaces import IgcPersonModifiedEvent
from gcommons.Users.config import PROJECTNAME
from gcommons.Users.config import PASSWORD_KEY



logger = logging.getLogger('gcommons.Users.content.gcPerson')



gcPersonSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.StringField(
        name='firstName',
        widget=atapi.StringWidget(
            label=u"First Name",
        ),
        required=True,
        schemata="Basic Information",
        searchable=True
    ),
    
    atapi.StringField(
        name='middleName',
        widget=atapi.StringWidget(
            label=_(u"FacultyStaffDirectory_label_middleName", default=u"Middle Name"),
            i18n_domain='FacultyStaffDirectory',
        ),
        required=False,
        schemata="Basic Information",
        searchable=True
    ),
    
    atapi.StringField(
        name='lastName',
        widget=atapi.StringWidget(
            label=_(u"FacultyStaffDirectory_label_lastName", default=u"Last Name"),
            i18n_domain='FacultyStaffDirectory',
        ),
        required=True,
        schemata="Basic Information",
        searchable=True
    ),
    
    atapi.StringField(
        name='suffix',
        widget=atapi.StringWidget(
            label=_(u"FacultyStaffDirectory_label_suffix", default=u"Suffix"),
            description=_(u"FacultyStaffDirectory_description_suffix", default=u"Academic, professional, honorary, and social suffixes."),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Basic Information",
        searchable=True
    ),
    
    atapi.StringField(
        name='email',
        required = True,
        user_property=True,
        widget=atapi.StringWidget(
            label=_(u"FacultyStaffDirectory_label_email", default=u"Email"),
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Basic Information",
        searchable=True,
        validators=('isEmail',)
    ),
    
#    
#    atapi.StringField(
#        name='officeAddress',
#        widget=atapi.TextAreaWidget(
#            label=_(u"FacultyStaffDirectory_label_officeAddress", default=u"Office Street Address"),
#            i18n_domain='FacultyStaffDirectory',
#        ),
#        schemata="Contact Information",
#        searchable=True
#    ),
#    
#    atapi.StringField(
#        name='officeCity',
#        widget=atapi.StringWidget(
#            label=_(u"FacultyStaffDirectory_label_officeCity", default=u"Office City"),
#            i18n_domain='FacultyStaffDirectory',
#        ),
#        schemata="Contact Information",
#        searchable=True
#    ),
#    
#    atapi.StringField(
#        name='officeState',
#        widget=atapi.StringWidget(
#            label=_(u"FacultyStaffDirectory_label_officeState", default=u"Office State"),
#            i18n_domain='FacultyStaffDirectory',
#        ),
#        schemata="Contact Information"
#    ),
#    
#    atapi.StringField(
#        name='officePostalCode',
#        widget=atapi.StringWidget(
#            label=_(u"FacultyStaffDirectory_label_officePostalCode", default=u"Office Postal Code"),
#            i18n_domain='FacultyStaffDirectory',
#        ),
#        schemata="Contact Information"
#    ),
#    
#    atapi.StringField(
#        name='officePhone',
#        widget=atapi.StringWidget(
#            label=_(u"FacultyStaffDirectory_label_officePhone", default=u"Office Phone"),
#            description=_(u"FacultyStaffDirectory_description_officePhone", default=u""),
#            i18n_domain='FacultyStaffDirectory',
#        ),
#        schemata="Contact Information",
#        searchable=True,
#    ),
    
    atapi.ImageField(
        name='image',
        schemata="Basic Information",
        widget=atapi.ImageWidget(
            label=_(u"FacultyStaffDirectory_label_image", default=u"Image"),
            i18n_domain='FacultyStaffDirectory',
            default_content_type='image/gif',
        ),
        storage = atapi.AttributeStorage(),
        original_size = (400, 500),
        sizes={'thumb': (100, 125), 'normal': (200, 250)},
        default_output_type='image/jpeg',
        allowable_content_types=('image/gif','image/jpeg','image/png'),
    ),
    
#    atapi.TextField(
#        name='biography',
#        widget=atapi.RichWidget(
#            label=_(u"FacultyStaffDirectory_label_biography", default=u"Biography"),
#            i18n_domain='FacultyStaffDirectory',
#        ),
#        schemata="Professional Information",
#        searchable=True,
#        validators=('isTidyHtmlWithCleanup',),
#        default_output_type='text/x-html-safe',
#        user_property='description'
#    ),
    
    
    
    atapi.ComputedField(
        name='title',
        widget= atapi.ComputedWidget (
            label=_(u"FacultyStaffDirectory_label_fullName", default=u"Full Name"),
            visible={'edit': 'invisible', 'view': 'visible'},
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Basic Information",
        accessor="Title",
        user_property='fullname',
        searchable=True
    ),
    
    atapi.StringField(
        name='id',
        widget=atapi.StringWidget(
            label=_(u"gcUser_label_id", default=u"Access Account ID"),
            i18n_domain='gcommons.User',
            description=_(u"gcUser_description_id", default=u"Example: abc123"),
        ),
        required=True,
        user_property=True,
        schemata="Basic Information",
#        write_permission=CHANGE_PERSON_IDS,
    ),

    atapi.StringField('password',
        languageIndependent=True,
        required=False,
        mode='w',
        write_permission=SetOwnPassword,
        widget=atapi.PasswordWidget(
            label=_(u"gcUser_label_password", default=u"Password"),
            description=_(u"gcUser_description_password", default=u"Password for this person (Leave blank if you don't want to change the password.)"),
            i18n_domain='gcommons.User',
            #condition="python:here.facultystaffdirectory_tool.getUseInternalPassword() and 'FSDPerson' in here.facultystaffdirectory_tool.getEnableMembraneTypes()"
        ),
        schemata="Basic Information",
    ),
    
    atapi.StringField('confirmPassword',
        languageIndependent=True,
        required=False,
        mode='w',
        write_permission=SetOwnPassword,
        widget=atapi.PasswordWidget(
            label=_(u"FacultyStaffDirectory_label_confirmPassword", default=u"Confirm password"),
            description=_(u"FacultyStaffDirectory_description_confirmPassword", default=u"Please re-enter the password. (Leave blank if you don't want to change the password.)"),
            i18n_domain='FacultyStaffDirectory',
            condition="python:here.facultystaffdirectory_tool.getUseInternalPassword() and 'FSDPerson' in here.facultystaffdirectory_tool.getEnableMembraneTypes()"
        ),
        schemata="Basic Information",
    ),
    
#    StringField('userpref_language',
#        widget=SelectionWidget(
#            label=_(u"label_language", default=u"Language"),
#            description=_(u"help_preferred_language", default=u"Your preferred language."),
#            i18n_domain='plone',
#            condition="python:'FSDPerson' in here.facultystaffdirectory_tool.getEnableMembraneTypes()"
#        ),
#        write_permission=SetOwnProperties,
#        schemata="User Settings",
#        vocabulary="_availableLanguages",
#        user_property='language',
#    ),
#    
#    StringField('userpref_wysiwyg_editor',
#        widget=SelectionWidget(
#            label=_(u"label_content_editor", default=u"Content editor"),
#            description=_(u"help_content_editor", default=u"Select the content editor that you would like to use. Note that content editors often have specific browser requirements."),
#            i18n_domain='plone',
#            format="select",
#            condition="python:'FSDPerson' in here.facultystaffdirectory_tool.getEnableMembraneTypes()"
#        ),
#        write_permission=SetOwnProperties,
#        schemata="User Settings",
#        vocabulary="_availableEditors",
#        user_property='wysiwyg_editor',
#    ),
#    
#    BooleanField('userpref_ext_editor',
#        widget=BooleanWidget(
#            label=_(u"label_ext_editor", default=u"Enable external editing"),
#            description=_(u"help_content_ext_editor", default=u"When checked, an icon will be made visible on each page which allows you to edit content with your favorite editor instead of using browser-based editors. This requires an additional application called ExternalEditor installed client-side. Ask your administrator for more information if needed."),
#            i18n_domain='plone',
#            condition="python:here.portal_properties.site_properties.ext_editor and 'FSDPerson' in here.facultystaffdirectory_tool.getEnableMembraneTypes()",
#            ),
#            write_permission=SetOwnProperties,
#            schemata="User Settings",
#            user_property='ext_editor',
#    ),
#    BooleanField('userpref_invisible_ids',
#        widget=BooleanWidget(
#            label=_(u"label_edit_short_names", default=u"Allow editing of Short Names"),
#            description=_(u"help_display_names", default=u"Determines if Short Names (also known as IDs) are changable when editing items. If Short Names are not displayed, they will be generated automatically."),
#            i18n_domain='plone',
#            condition="python:here.portal_properties.site_properties.visible_ids and 'FSDPerson' in here.facultystaffdirectory_tool.getEnableMembraneTypes()"
#            ),
#            write_permission=SetOwnProperties,
#            schemata="User Settings",
#            user_property='invisible_ids',
#    ),
))


def finalizegcPersonSchema(Schema):
    Schema['title'].storage = atapi.AnnotationStorage()
    Schema['description'].storage = atapi.AnnotationStorage()
    
    schemata.finalizeATCTSchema(Schema, moveDiscussion=False)
    
    Schema.changeSchemataForField('description', 'metadata')    
    return Schema


class gcPersonModifiedEvent(object):
    """ Event that happens when edits to a Person have been saved
        stolen from FacultyStaffDirectory
    """
    implements(IgcPersonModifiedEvent)
    
    def __init__(self, context):                      
        self.context = context
           

class gcPerson(base.ATCTContent):
    """A user of gcommons"""

    security = ClassSecurityInfo()
    meta_type = "gcPerson"
    schema = finalizegcPersonSchema(gcPersonSchema)

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    
    implements(IgcPerson,
               IUserAuthProvider,
               IPropertiesProvider,
               IGroupsProvider,
               IGroupAwareRolesProvider,
               IAttributeAnnotatable,
               IUserChanger)
    

    """
    Methods to support notifications
    """
    security.declareProtected(View, 'at_post_create_script')
    def at_post_create_script(self):
        """Notify that the Person has been modified.
        """
        notify(gcPersonModifiedEvent(self))

    security.declareProtected(View, 'at_post_edit_script')
    def at_post_edit_script(self):
        """Notify that the Person has been modified.
        """
        notify(gcPersonModifiedEvent(self))

    """
    Methods for standard interface
    """
    def __call__(self, *args, **kwargs): 
        #  member like behaviour (return string)    
        return self.getId()
    
    
    
    security.declareProtected(View, 'vcard_view')
    def vcard_view(self, REQUEST, RESPONSE):
        """vCard 3.0 output
        """
        RESPONSE.setHeader('Content-Type', 'text/x-vcard')
        RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s.vcf"' % self.getId())
        out = StringIO()
        
        # Get the fields using the accessors, so they're properly Unicode encoded.
        out.write("BEGIN:VCARD\nVERSION:3.0\n")
        out.write("FN:%s\n" % self.Title())
        out.write("N:%s;%s\n" % (self.getLastName(), self.getFirstName()))
        out.write(foldLine("TITLE:%s\n" % '\\n'.join(self.getJobTitles())))
        out.write(foldLine("ADR;TYPE=dom,postal,parcel,work:;;%s;%s;%s;%s\n" % (self.getOfficeAddress().replace('\r\n','\\n'), self.getOfficeCity(), self.getOfficeState(), self.getOfficePostalCode())))
        out.write("TEL;WORK:%s\n" % self.getOfficePhone())
        out.write("EMAIL;TYPE=internet:%s\n" % self.getEmail())
        
        #Add the Person page to the list of URLs
        urls = list(self.getWebsites())
        urls.append(self.absolute_url())
        for url in urls:
            out.write(foldLine("URL:%s\n" % url))
        if self.getImage():
            encData = self.image_thumb.data.encode('base-64')
            # indent the data block:
            indentedData = '\n  '.join(encData.strip().split('\n'))
            out.write("PHOTO;ENCODING=BASE64;TYPE=JPEG:\n  %s\n" % indentedData)
        out.write("REV:%s\n" % DateTime(self.ModificationDate()).ISO8601())
        out.write("PRODID:WebLion Faculty/Staff Directory\nEND:VCARD")
        return n2rn(out.getvalue())
    
    security.declareProtected(View, 'getSortableName')
    def getSortableName(self):
        """
        Return a tuple of the person's name. For sorting purposes
        Return them as lowercase so that names like 'von Whatever' sort properly
        """
        return (self.lastName.lower(), self.firstName.lower())
    
    security.declareProtected(View, 'Title')
    def Title(self):
        """Return the Title as firstName middleName(when available) lastName, suffix(when available)"""
        try:
            # Get the fields using the accessors, so they're properly Unicode encoded.
            # We also can't use the %s method of string concatentation for the same reason.
            # Is there another way to manage this?
            fn = self.getFirstName()
            ln = self.getLastName()
        except AttributeError:
            return u"new person" # YTF doesn't this display on the New Person page?  # Couldn't call superclass's Title() for some unknown reason
        
        if self.getMiddleName():
            mn = " " + self.getMiddleName() + " "
        else:
            mn = " "
        
        t = fn + mn + ln
        if self.getSuffix():
            t = t + ", " + self.getSuffix()
        
        return t
        
    security.declarePrivate('_availableEditors')
    def _availableEditors(self):
        """ Return a list of the available WYSIWYG editors for the site. """
        props = getToolByName(self, 'portal_properties')
        return props['site_properties'].available_editors
    
    security.declarePrivate('_availableLanguages')
    def _availableLanguages(self):
        """ Return a list of the available languages for the site. """
        props = getToolByName(self, 'portal_properties')
        return props.availableLanguages()

    def getLoginRedirect(self):
        logger.info("Redirecting!")
        return self.absolute_url() + '/view'
        
#    security.declareProtected(View, 'tag')
#    def tag(self, **kwargs):
#        """Pass along the 'tag' method to the Person's image."""
#        return self.getWrappedField('image').tag(self, **kwargs)
#    
#    security.declareProtected(View, 'getImageOfSize')
#    def getImageOfSize(self, height, width, **kwargs):
#        """Return the person's image sized to the given dimensions."""
#        return self.getWrappedField('image').tag(self, width=width, height=height, **kwargs)
#    
#    security.declareProtected(View, 'getScaledImageByWidth')
#    def getScaledImageByWidth(self, preferredWidth, **kwargs):
#        """Return the person's image sized to the given width and a height scaled according to the original image ratio. Fail nicely, returning no image tag. This seems to occur when TIFF images are used."""
#        if not (self.image.height or self.image.width):
#            logger.error("There was an error resizing the image for person %s" % self)
#            return ''
#        hwratio = float(self.image.height)/float(self.image.width)
#        calcHeight = int(preferredWidth * hwratio)
#        return self.getImageOfSize(calcHeight, preferredWidth, **kwargs)
#    
#    security.declareProtected(ModifyPortalContent, 'setImage')
#    def setImage(self, value, **kwargs):
#        field = self.getField('image')
#        
#        # If the image exists in portal memberdata's portraits folder, delete it
#        md = getToolByName(self, 'portal_memberdata')
#        if md.portraits.has_key(self.id):
#            md.portraits._delObject(self.id)
#        
#        # Assign the image to the field
#        field.set(self, value)
#        
#        # If there is an image value (not the empty string that seems to get sent on object creation)
#        # and it's not a delete command, create a member portrait
#        if value and value != 'DELETE_IMAGE':
#            # Add the new portrait
#            md.portraits._setObject(id=self.id, object=self.getImage())
#    

    security.declareProtected(SetOwnPassword, 'setPassword')
    def setPassword(self, value):
        """"""
        if value:
            annotations = IAnnotations(self)
            annotations[PASSWORD_KEY] = sha(value).digest()
    
    security.declareProtected(SetOwnPassword, 'setConfirmPassword')
    def setConfirmPassword(self, value):
        """"""
        # Do nothing - this value is used for verification only
        pass

    
    security.declarePrivate('validate_officePhone')
    def validate_officePhone(self, value=None):
        """ Make sure the phone number fits the regex defined in the configuration. """
        if value:
            fsd_tool = getToolByName(self, TOOLNAME)
            regexString = fsd_tool.getPhoneNumberRegex()
            if regexString and not re.match(regexString, value):
                return "Please provide the phone number in the format %s" % fsd_tool.getPhoneNumberDescription()

    
    security.declarePrivate('post_validate')
    def post_validate(self, REQUEST, errors):
        form = REQUEST.form
        if form.has_key('password') or form.has_key('confirmPassword'):
            password = form.get('password', None)
            confirm = form.get('confirmPassword', None)
            
            annotations = IAnnotations(self)
            passwordDigest = annotations.get(PASSWORD_KEY, None)
            
            if not passwordDigest:
                if not password and not confirm:
                    errors['password'] = u'An initial password must be set'
                    return
            if password or confirm:
                if password != confirm:
                    errors['password'] = errors['confirmPassword'] = u'Passwords do not match'
                    

# Implementing IMultiPageSchema forces the edit template to render in the more Plone 2.5-ish manner,
# with actual links at the top of the page instead of Javascript tabs. This allows us to direct people
# immediately to a specific fieldset with a ?fieldset=somethingorother query string. Plus, it also
# gives the next/previous links at the bottom of the form.
try:
    from Products.Archetypes.interfaces import IMultiPageSchema
except ImportError:
    # It doesn't exist, do nothing
    pass
else:
    classImplements(gcPerson, IMultiPageSchema)
    pass

atapi.registerType(gcPerson, PROJECTNAME)

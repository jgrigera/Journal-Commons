from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from gcommons.deutscher import MessageFactory as _


# Interface class; used to define content-type schema.
class IDeutscherHomepage(form.Schema, IImageScaleTraversable):
	"""
	Homepage for Deutscher Prize
	"""
	maintext = RichText(
		title=_(u"Main text"),
		required=False
	)
	banner01 = NamedImage(
		title=_(u"First Banner Image"),
		description=_(u"Please upload an image sized 1000x526"),
		required=False,
	)
	banner02 = NamedImage(
		title=_(u"Second Banner Image"),
		description=_(u"Please upload an image"),
		required=False,
	)



class DeutscherHomepage(dexterity.Item):
    grok.implements(IDeutscherHomepage)
    
    # Add your class methods and properties here


# View class
grok.templatedir('templates')

class DeutscherHomepageView(grok.View):
    grok.context(IDeutscherHomepage)
    grok.require('zope2.View')
    grok.name('view')

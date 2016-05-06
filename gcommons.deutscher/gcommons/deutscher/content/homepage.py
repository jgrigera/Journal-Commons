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

import logging

logger = logging.getLogger('gcommons.deutscher.content.homepage')
from gcommons.deutscher import MessageFactory as _

# TODO: how to make this useful
BannerSizes = {'large': (768, 768),
              'preview': (400, 400),
              'mini': (200, 200),
              'thumb': (128, 128),
              'tile': (64, 64),
              'icon': (32, 32),
              'listing': (16, 16),
              'banner': (1000, 526),
}


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
		required=True,
	)
	banner02 = NamedImage(
		title=_(u"Second Banner Image"),
		description=_(u"Please upload an image"),
		required=True,
	)
	banner03 = NamedImage(
		title=_(u"Third Banner Image"),
		description=_(u"Please upload an image"),
		required=True,
	)



class DeutscherHomepage(dexterity.Item):
    grok.implements(IDeutscherHomepage)
    
    def getAvailableSizes(self):
		logger.info("HHHHHHHHHHH")
    
    # Add your class methods and properties here


# View class
grok.templatedir('templates')

class DeutscherHomepageView(grok.View):
    grok.context(IDeutscherHomepage)
    grok.require('zope2.View')
    grok.name('view')

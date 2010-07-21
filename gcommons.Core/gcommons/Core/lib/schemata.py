

from Products.Archetypes import atapi
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.DataGridField.DataGridWidget import DataGridWidget
from Products.DataGridField.DataGridField import DataGridField


#TODO: WTF!!!
from journalcommons.Conference import ConferenceMessageFactory as _


gcAuthorsSchema_basic = atapi.Schema ((
    atapi.StringField(
        name='primaryAuthor',
        searchable=True,
        index='FieldIndex',
        default_method ='_compute_author',
        vocabulary = 'vocabAuthor',
        storage = atapi.AnnotationStorage(),
        widget = atapi.ComputedWidget(
            name = 'Primary Author',
            description = _('Principal creator or responsible of the paper.'),
            visible = {'edit' : 'visible', 'view' : 'visible' },
        ),
    ),

    DataGridField(
        name='unconfirmedExtraAuthors',
        widget=DataGridWidget(
            label=_("Other Authors"),
            description = _('If applicable, other authors of the paper or persons responsible for this piece, besides the principal author.'),
            column_names=('Name', 'Institution', 'email'),
        ),
        allow_empty_rows=False,
        required=False,
        columns=('name', 'institution', 'email')
    ),

#    atapi.ReferenceField(
#        name='refExtraAuthors',
#        relationship = 'refExtraAuthors',
#        required = False,
#        multiValued = True,
#        searchable=1,
#        allowed_types=('gcPerson',),
#        storage=atapi.AnnotationStorage(),
#        
#        widget = ReferenceBrowserWidget(
#            label=_("Other Authors"),
#            description = _('If applicable, other authors of the paper or persons responsible for this piece, besides the principal author.'),
#            allow_browse=0,
#            allow_search=1,
#            show_results_without_query=1, 
##            startup_directory_method="_get_gcommons_users_tool",
#        ),            
#    ),
    

#    atapi.ComputedField(
#        name='creators',
#        storage = atapi.AnnotationStorage(),
#        searchable = True,
#        expression = 'context._compute_creators()',
#    ),
))



def finalizeAuthorsSchema(schema):
	"""
	fix and finish Authors Schema
	"""
	
	schema.delField('refExtraAuthors')
	return schema

	# First of all, do we have gcommons.Users installed?
	#if gcommons.Users not installed:
		# extraAuthors is all you've got 
		# invitations are not possible
		# i.e. confirmEmails = False, allowInvitations = False
	#	remove refExtraAuthors
		#	TODO: in the future we could alllow referencing of plain Plone Users
	#	return
		
	# If gcommons.Users is installed you can choose to confirm Emails or not, and allow invitations or not
	# condition:
	#    confirmEmails: leave as is

	# if   allowInvitations: leave as is
	# else
	# 		remove
	#return Schema


#gcAuthorsSchema = finalizeAuthorsSchema(gcAuthorsSchema_basic)
gcAuthorsSchema = gcAuthorsSchema_basic



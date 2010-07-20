

from Products.Archetypes import atapi
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.DataGridField.DataGridWidget import DataGridWidget
from Products.DataGridField.DataGridField import DataGridField


#TODO: WTF!!!
from journalcommons.Conference import ConferenceMessageFactory as _


gcAuthorsSchema_no_membrane = atapi.Schema ((
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
        name='extraAuthors',
        widget=DataGridWidget(
            label=_("Other Authors"),
            description = _('If applicable, other authors of the paper or persons responsible for this piece, besides the principal author.'),
            column_names=('Name', 'Institution',),
        ),
        allow_empty_rows=False,
        required=False,
        columns=('name', 'institution')
    ),

    atapi.ComputedField(
        name='creators',
        storage = atapi.AnnotationStorage(),
        searchable = True,
        expression = 'context._compute_creators()',
    ),
))


gcAuthorsSchema_ref = atapi.Schema ((
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

    atapi.ReferenceField(
        name='extraAuthors',
        relationship = 'refExtraAuthors',
        required = False,
        multiValued = True,
        searchable=1,
        allowed_types=('gcPerson',),
        storage=atapi.AnnotationStorage(),
        
        widget = ReferenceBrowserWidget(
            label=_("Other Authors"),
            description = _('If applicable, other authors of the paper or persons responsible for this piece, besides the principal author.'),
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1, 
#            startup_directory_method="_get_gcommons_users_tool",
        ),            
    ),
    

#    atapi.ComputedField(
#        name='creators',
#        storage = atapi.AnnotationStorage(),
#        searchable = True,
#        expression = 'context._compute_creators()',
#    ),
))



                                                  

gcAuthorsSchema = gcAuthorsSchema_ref
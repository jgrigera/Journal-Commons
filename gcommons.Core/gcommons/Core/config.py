"""Common configuration constants
"""
import permissions

PROJECTNAME = 'gcommons.Core'

ADD_PERMISSIONS = {
    # -*- extra stuff goes here -*-
    'CallForPapers': 'gcommons.Core: Add CallForPapers',
    'SubmissionsFolder': 'gcommons.Core: Add SubmissionsFolder',

    'Draft':   permissions.AddDraft,
    'Comment': permissions.AddComment,
}

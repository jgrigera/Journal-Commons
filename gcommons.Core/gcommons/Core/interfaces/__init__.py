
# -*- extra stuff goes here -*-
# Content Types
from comment import IComment
from draft import IDraft
from submissionsfolder import ISubmissionsFolder
from callforpapers import ICallForPapers

# 
# buildout breaks, unless i comment this out. no idea what it does
# though. -toni.  
# from jcommonsSubmittable import IjcommonsSubmittable
from container import IgcContainer, IgcContainerModifiedEvent



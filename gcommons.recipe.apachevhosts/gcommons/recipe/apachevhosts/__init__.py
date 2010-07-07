# -*- coding: utf-8 -*-
"""Recipe apachevhosts"""

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        print "///////////////////"
        print "Hello: %s" % self.name

    def install(self):
        """Installer"""
        # XXX Implement recipe functionality here
        print "///////////////////"
        print "Hello: %s" % self.name
        
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple()

    def update(self):
        """Updater"""
        print "///////////////////"
        print "Hello: %s" % self.name


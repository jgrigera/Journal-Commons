# -*- coding: utf-8 -*-
"""Recipe apachevhosts"""

from datetime import datetime
import logging
import os


default_template = """
#
#
# DO NOT MODIFY THIS BY HAND
# AUTOMATICALLY GENERATED DURING BUILDOUT
# YOUR CHANGES *WILL* BE LOST
#
# Buildout dir: %(buildout)s
# Buildout part: %(part)s
# Last update:  %(timestamp)s
#
<VirtualHost *:80>
    ServerName %(url)s
    %(urlalias)s

    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>

    ProxyPass / http://%(httpaddress)s/VirtualHostBase/http/%(url)s:80/%(path)s/VirtualHostRoot/
    ProxyPassReverse / http://%(httpaddress)s/VirtualHostBase/http/%(url)s:80/%(path)s/VirtualHostRoot/

    <Directory />
        Options FollowSymLinks
        AllowOverride None
    </Directory>

</VirtualHost>

"""

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.logger = logging.getLogger(name)

    def install(self):
        """Installer"""
        return self.writeVhosts()

    def update(self):
        """Updater"""
        self.writeVhosts()
        
    def writeVhosts(self):
        files = []
        vhosts = self.options['vhosts']
        httpaddress =  self.options['http-address']
        outputdir = self.options['outputdir']
        prefix = self.options.get('prefix')
        postfix = self.options.get('postfix')
        template = self.options.get('template')

        for line in vhosts.split('\n'):
            if len(line.split()):
        	site, path, url = line.split()
        	if prefix is not None:
        	    url = "%s.%s" % (prefix, url)
        	if postfix is not None:
        	    url = "%s.%s" % (site, postfix)
        	    
        	values = dict()
        	values['buildout'] = self.buildout['buildout']['directory']
        	values['httpaddress'] = httpaddress
        	values['site'] = site
        	values['path'] = path
        	values['url'] = url
        	values['part'] = self.name
        	values['timestamp'] = str(datetime.now())[0:16]
        	
        	# Provide non-'www.' alias directive
        	if url[0:4] == 'www.':
        	    values['urlalias'] = 'ServerAlias %s' % url[4:]
        	else:
        	    values['urlalias'] = ""
        	
        	# Use provided template or default
        	if template is None:
        	    template = default_template
        	filename = os.path.join(outputdir, "%s.conf" % site)
        	files.append(filename)
        	out = open(filename, "w")
        	out.write(template % values)
        	out.close()

        return files


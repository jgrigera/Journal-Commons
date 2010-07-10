# -*- coding: utf-8 -*-
"""
This module contains the tool of gcommons.recipe.apachevhosts
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = read('version.txt')

long_description = (
    read('README.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('gcommons', 'recipe', 'apachevhosts', 'README.txt')
    + '\n' +
    'Contributors\n' 
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' + 
    read('CHANGES.txt')
    + '\n' +
   'Download\n'
    '********\n'
    )
entry_point = 'gcommons.recipe.apachevhosts:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require=['zope.testing', 'zc.buildout']

setup(name='gcommons.recipe.apachevhosts',
      version=version,
      description="buildout recipe that writes apache.conf virtual hosts",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      keywords='',
      author='Juan Grigea',
      author_email='juan@grigera.com.ar',
      url='http://www.gcommons.org',
      license='AGPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gcommons', 'gcommons.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'gcommons.recipe.apachevhosts.tests.test_docs.test_suite',
      entry_points=entry_points,
      )

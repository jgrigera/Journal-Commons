# -*- coding: utf-8 -*-
"""
This module contains the tool of JournalCommons
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = read('version.txt')

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read("docs", "HISTORY.txt")
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('gcommons', 'Journal', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n')

tests_require = ['zope.testing']

setup(name='gcommons.Journal',
      version=version,
      description="gcommons product to run a Journal or Magazine",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='journal',
      author='Juan Grigera,Toni Prug',
      author_email='contact@gcommons.org',
      url='http://github.com/jgrigera/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gcommons', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
			'Products.DataGridField',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'gcommons.Journal.tests.test_docs.test_suite',
      entry_points="""
      # -*- entry_points -*- 
      [distutils.setup_keywords]
      paster_plugins = setuptools.dist:assert_string_list

      [egg_info.writers]
      paster_plugins.txt = setuptools.command.egg_info:write_arg
      """,
      paster_plugins = ["ZopeSkel"],
      )

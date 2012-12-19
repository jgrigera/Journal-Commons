from setuptools import setup, find_packages
import os

version = '1.0'

setup(
        name='gcommons.theme.deutscher',
        description='Deutscher Site installable Diazo theme for Plone 4.2+',
        long_description=open('README.rst', 'rb').read()+'\n'+
                         open(os.path.join("docs", "INSTALL.txt")).read()+'\n'+
                         open(os.path.join("docs", "HISTORY.txt")).read(),
        version='1.0',
        author='Juan Grigera',
        author_email='juan@grigera.com.ar',
        url='http://svn.plone.org/svn/collective/',
        packages=find_packages(),
        include_package_data=True,
        namespace_packages=['gcommons', 'gcommons.theme'],
        install_requires=[
            'setuptools',
            'plone.app.theming',
            ],
        classifiers=[
            "Framework :: Plone",
            "Programming Language :: Python",
            ],
        entry_points={
            'z3c.autoinclude.plugin': 'target = plone',
            }
        )


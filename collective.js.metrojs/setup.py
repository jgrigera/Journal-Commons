from setuptools import setup, find_packages

version = '0.8.9.3l'

setup(
    name='collective.js.metrojs',
    version=version,
    description="metroJS package integration for Plone",
    long_description=open("README.rst").read(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    keywords='Plone jQuery MetroJS',
    author='Juan Grigera',
    author_email='info@gcommons.org',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['collective', 'collective.js'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Products.CMFCore',
        'Products.GenericSetup',
    ],
    entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
    """,
    extras_require={'test': ['plone.app.testing']},
)

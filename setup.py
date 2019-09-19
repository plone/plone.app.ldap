# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '1.4.4'

setup(name='plone.app.ldap',
      version=version,
      description="LDAP control panel for Plone 4.2 and higher",
      long_description=(open("README.rst").read() + "\n" +
                        open("CHANGES.rst").read()),
      classifiers=[
          "Development Status :: 6 - Mature",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP",
          ],
      keywords='plone ldap',
      author='Wichert Akkerman - Simplon',
      author_email='wichert@simplon.biz',
      maintainer='Kevin Teague',
      maintainer_email='kevin@bud.ca',
      url='https://github.com/plone/plone.app.ldap',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'plone.memoize',
          'Products.CMFCore',
          'Products.CMFDefault',
          'Products.GenericSetup >= 1.8.2',
          'Products.PloneLDAP',
          'python-ldap',
          'setuptools',
          'six',
          'zope.component',
          'plone.app.form',
          'five.formlib',
          'zope.formlib',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.lifecycleevent',
          'zope.schema',
      ],
      extras_require={
          'test': [
            'plone.api',
            'plone.app.testing',
            'plone.testing',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

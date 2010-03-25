from setuptools import setup, find_packages

version = '1.2'

setup(name='plone.app.ldap',
      version=version,
      description="LDAP control panel for Plone 3",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP",
        ],
      keywords='plone ldap',
      author='Wichert Akkerman - Simplon',
      author_email='wichert@simplon.biz',
      url='http://pypi.python.org/pypi/plone.app.ldap',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
#          "python-ldap",
          "Products.PloneLDAP",
          "setuptools"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

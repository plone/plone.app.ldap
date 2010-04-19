LDAP control panel for Plone
============================

Overview
--------

plone.app.ldap provides a user interface in a Plone site to manage
LDAP and Active Directory servers. 

This package succeeds the simplon.plone.ldap package.

It builds on the functionality provided by LDAPMultiPlugins_, LDAPUserFolder_
and PloneLDAP_.


Active Directory
----------------

Active Directory provides an LDAP interface to its data. Using this interface
Plone can use both users and groups from an Active Directory system. Writing
to Active Directory is not supported.

With Active Directory you can use two different properties as login name:
`userPrincipalName` and `sAMAccountName`. `sAMAccountName` is the plain account
name without any domain information and is only unique within a single domain.
If your environment only uses a single AD domain this option is the best
choice. For environments with multiple names the `userPrincipalName` attribute
can be used since this includes both account name and domain information.


Since Plone does not support binary user ids it is not possible to use the
`objectGUID` attribute as user ids. Instead you can use either `sAMAccountName`
or `userPrincipalName`. The same criteria for choosing a login name also
apply to selecting the user id attribute.

Standard LDAP
-------------

LDAP directory servers are fully supported. LDAP users and groups are usable
as standard Plone users and groups can be me managed normally. Creating and
deleting users and groups is supported.


Installing
----------

This package works with Plone 3 and Plone 4. Plone 3 users should install a version in the 1.2.* series (e.g. plone.app.ldap < 1.3), as releases after version 1.3 will only work with Plone 4.

You need to install PloneLDAP_ and its requirements in your Zope instance
before you can use plone.app.ldap. This can easily be done by downloading
its product bundle and extracting that in your Products directory.

Once the package is installed, it will be available as an add-on named
"LDAP support", and this add-on can be activated in a Plone instance
using the Add-ons section of the Plone Control Panel. Be careful, as this
package also currently installs LDAPUserFolder as a dependency, which makes
the add-on "LDAPUserFolder CMF Tools" available. Do not install this add-on!
It will replace the portal_membership tool and make your Plone site
unusable.

Install without buildout
~~~~~~~~~~~~~~~~~~~~~~~~

First you need to install this package in the python path for your
Zope instance. This can be done by installing it in either your system
path packages or in the lib/python directory in your Zope instance.

After installing the package it needs to be registered in your Zope instance.
This can be done by putting a plone.app.ldap-configure.zcml file in the
etc/pakage-includes directory with this content::

  <include package="plone.app.ldap" />

or, alternatively, you can add that line to the configure.zcml in a
package or Product that is already registered.

Installing with buildout
~~~~~~~~~~~~~~~~~~~~~~~~

If you are using `buildout`_ to manage your instance installing plone.app.ldap 
is even simpler. You can install it by adding it to the eggs line for your 
instance::

  [instance]
  eggs = plone.app.ldap
  zcml = plone.app.ldap

The last line tells buildout to generate a zcml snippet that tells Zope to 
configure plone.app.ldap.

.. _buildout: http://pypi.python.org/pypi/zc.buildout


Installing the development version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To specify the current `development`_ version you may use::

  eggs = plone.app.ldap==dev

.. _development: https://svn.plone.org/svn/plone/plone.app.ldap/trunk#egg=plone.app.ldap-dev


Copyright and credits
---------------------

Copyright
    plone.app.ldap is Copyright 2007, 2008 by the Plone Foundation.
    Simplon_ donated the simplon.plone.ldap code to the Plone Foundation.

Credits
     Wichert Akkerman <wicher@simplon.biz>

Funding
     CentrePoint_


.. _simplon: http://www.simplon.biz/
.. _python-ldap: http://python-ldap.sourceforge.net/
.. _LDAPUserFolder: http://www.dataflake.org/software/ldapuserfolder/
.. _LDAPMultiPlugins: http://www.dataflake.org/software/ldapmultiplugins/
.. _PloneLDAP: http://plone.org/products/ploneldap/
.. _CentrePoint: http://centrepoint.org.uk/

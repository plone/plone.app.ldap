LDAP control panel for Plone
============================

.. image:: https://travis-ci.org/plone/plone.app.ldap.svg?branch=master
   :target: https://travis-ci.org/plone/plone.app.ldap

.. image:: https://coveralls.io/repos/github/plone/plone.app.ldap/badge.svg?branch=master
   :target: https://coveralls.io/github/plone/plone.app.ldap?branch=master

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
``userPrincipalName`` and ``sAMAccountName``. ``sAMAccountName`` is the plain
account name without any domain information and is only unique within a single
domain.  If your environment only uses a single AD domain this option is the
best choice. For environments with multiple names the ``userPrincipalName``
attribute can be used since this includes both account name and domain
information.

Since Plone does not support binary user ids it is not possible to use the
``objectGUID`` attribute as user ids. Instead you can use either
``sAMAccountName`` or ``userPrincipalName``. The same criteria for choosing a
login name also apply to selecting the user id attribute.

Newer versions of Active Directory may also work using the standard LDAP
plugin, which supports limited writing to AD, including modifying group
memberships.  If your group objects have ``member`` attributes containing the
user's full DN, the standard LDAP plugin should work for you.  Note that this
will not support nested groups.


Standard LDAP
-------------

LDAP directory servers are fully supported. LDAP users and groups are usable
as standard Plone users and groups can be me managed normally. Creating and
deleting users and groups is supported.


Installing
----------

This package works with Plone 3 and Plone 4. Plone 3 and Plone 4.0
users should install a version in the 1.2.* series
(e.g. plone.app.ldap < 1.3, the latest current release is 1.3.2), as
release 1.3 will only work with Plone 4.1 or higher.

This package depends on ``python-ldap``. In order to build it correctly you
need to have some development libraries included in your system. On a typical
Debian-based installation use::

    sudo apt-get install python-dev libldap2-dev libsasl2-dev libssl-dev

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
path packages (usually with ``pip`` or ``easy_install``) or in the
lib/python directory in your Zope instance.

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
zope instance::

  [instance]
  eggs =
      ...
      plone.app.ldap

.. _buildout: http://pypi.python.org/pypi/zc.buildout


Installing the development version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To specify the current development version you may use::

  [buildout]
  find-links =
      ...
      http://github.com/plone/plone.app.ldap/tarball/master#egg=plone.app.ldap-dev

  [instance]
  eggs =
      ...
     plone.app.ldap==dev

With ``pip`` that would be this::

  pip install -f http://github.com/plone/plone.app.ldap/tarball/master#egg=plone.app.ldap-dev plone.app.ldap==dev

With ``easy_install``::

  easy_install -f http://github.com/plone/plone.app.ldap/tarball/master#egg=plone.app.ldap-dev plone.app.ldap==dev


Copyright and credits
---------------------

Copyright
    plone.app.ldap is Copyright 2007, 2008 by the Plone Foundation.
    Simplon_ donated the simplon.plone.ldap code to the Plone Foundation.

Credits
     Wichert Akkerman <wichert@simplon.biz>

Funding
     CentrePoint_


.. _simplon: http://www.simplon.biz/
.. _python-ldap: http://python-ldap.sourceforge.net/
.. _LDAPUserFolder: http://www.dataflake.org/software/ldapuserfolder/
.. _LDAPMultiPlugins: http://www.dataflake.org/software/ldapmultiplugins/
.. _PloneLDAP: http://plone.org/products/ploneldap/
.. _CentrePoint: http://centrepoint.org.uk/

Changelog
=========

1.4.0 (2016-08-19)
------------------

New:

- Dropped support for Plone 4.1.
  [hvelarde]

- Added some more fields to portal_setup import/export, including
  extra_user_filter, group mappings, and plugin type (AD/non-AD).
  [adaugherity]

Fixes:

- Fix Travis CI build by pinning ``coverage`` and by ensuring different
  Plone versions are actually tested.
  [davidjb]

- Added ``metadata.xml`` to profile, plus empty upgrade step, so the
  add-ons control panel does not complain that we have no upgrade
  procedure.
  [maurits]

- Fixed plugin activation for AD; correctly add mandatory schema items; activate
  group management plugin for non-AD (to allow modifying group memberships via
  Plone).
  [adaugherity]

- Properly store settings made via control panel so that the control panel,
  ZMI, and portal_setup export all show the same data.
  [adaugherity]

- Miscellaneous minor bugfixes and documentation improvements.
  [adaugherity]

- Use zope.interface decorator.
  [gforcada]

1.3.2 (2015-03-02)
------------------

- Fix GS import : _user_objclasses and _roles should not be imported as unicode strings
  [gotcha]

- Update package dependencies.
  [hvelarde]

- Update installation documentation.
  [hvelarde]


1.3.1 (2013-10-01)
------------------

- Use ``.png`` file, not ``.gif``.  Fixes ``KeyError:
  confirm_icon.gif`` from
  https://github.com/plone/plone.app.ldap/issues/11
  [maurits]


1.3.0 (2012-09-28)
------------------

- Add Plone 4.3 compatibility, and break compatibility with Plone 4.0
  and Plone 3, by not importing from zope.app anymore.
  [maurits]

- Fix the exporter as GS 1.7 and higher now explicitly only
  understands strings.  Still works for older GS too.
  [sneridagh]


1.2.8 (2012-03-02)
------------------

- Added a z3c.autoinclude entry point to mark this as a Plone add-on.
  [WouterVH]


1.2.7 (2011-10-19)
------------------

- Expose the 'Read Only' attribute of LDAP plugins for modification with
  plone.app.ldap (http://dev.plone.org/ticket/12292)
  [kteague]

- Fix bug where changes to the Default User Roles option were being
  discarded (http://dev.plone.org/ticket/12293)
  [kteague]


1.2.6 (2011-07-17)
------------------

- Add Plone 4.1 compatibility when importing IVocabularyFactory.
  [fvandijk]

- Include Products.CMFCore for Plone 4.1 compatibility.
  [WouterVH]


1.2.5 (2011-05-02)
------------------

- Added import-support for activated interfaces, user_default_roles
  and password_encryption [awello]

- Update imports for zope.formlib bump in Plone 4.1
  [eleddy]

- Update GS import to support plugin id, and update parameter
  [eleddy]

- Update GS import to read interfaces config for AD plugins,
  apply cache parameter
  [eleddy]


1.2.4 (2010-12-07)
------------------

- Fix bug where generic setup exports were exporting boolean values
  as type int.
  [kteague]

- Fix bug where generic setup imports weren't choosing names correctly.
  [kteague]


1.2.3 (2010-10-07)
------------------

- Fix: Login Name, User ID  and RDN attributes were not set correctly on creation.
  [elro]


1.2.2 (2010-08-18)
------------------

- LDAPProperty fields can now be marked as a Binary property.
  [kteague]

- Ability to import/export an LDAP configuration using generic setup.
  This feature is the same as the one provided by collective.genericsetup.ldap
  and exports made with that product can be imported into plone.app.ldap.
  During import all existing servers, general settings and schema
  will be overwritten from config file - but no interfaces or cache
  settings are changed.
  [kteague]

- Removed locales directory. You can translate this package
  in the plone.app.locales package now.
  [vincentfretin]

- Cleaned templates to work with cmf.pt
  [pilz]


1.2.1 (2010-04-19)
------------------

- Fallback to Plone 3 compatible imports. Fix display of cache tab in Plone 3.
  [kteague]


1.2 (2010-03-25)
----------------

- Added a tab for display and modifying the cache settings.
  [kteague]

- Send out notification events for all object additions/modifications/removals
  so that configuration always gets propogated to the LDAPUserFolder object.
  [kteague]

- Changed the base class for LDAPConfiguration so that it gets properly
  rooted in the site (otherwise LDAPConfiguration.__parent__ goes into
  an infinite loop, pointing to a fresh PersistenComponents instance who's
  parent is in turn LDAPConfiguration).
  [kteague]

- Updated the HTML to wrap all control panel forms in a form tag so that
  tabs are properly displayed in Plone 4.
  [kteague]

- Fixed i18n domain changes from Vincent. The message factory was defined in
  the wrong ``__init__.py``.
  [hannosch]

- Changed i18n domain from plone to plone.app.ldap.
  Registered locales directory.
  [vincentfretin]


1.1 (2008-08-16)
----------------

- Fix ldap schema config for Active Directory
  [elro]


simplon.plone.ldap - 1.0
------------------------

- Initial package structure.
  [zopeskel]

# -*- coding: utf-8 -*-
from plone.app.ldap.engine.interfaces import ILDAPConfiguration
from Products.CMFCore.utils import getToolByName
import logging


logger = logging.getLogger(__name__)


def uninstall(context):
    """Uninstall script"""
    PLUGIN_ID = "ldap-plugin"
    pas = getToolByName(context, 'acl_users')

    # Remove plugin if it exists.
    if PLUGIN_ID in pas.objectIds():
        pas._delObject(PLUGIN_ID)
        logger.info('Removed LDAP plugin %s from acl_users.', PLUGIN_ID)

    portal = getToolByName(context, 'portal_url').getPortalObject()
    sm = portal.getSiteManager()
    # The removal in profiles/uninstall/componentregistry.xml does not work correctly,
    # or not enough.  Presumably this is because the registration contains a factory,
    # which generates a component on the fly, so the real component
    # is never actually unregistered.  In code it also has no effect:
    # sm.unregisterUtility(factory=LDAPConfiguration, provided=ILDAPConfiguration)
    # So instead we get the real utility.
    # getUtility(ILDAPConfiguration) already may not work,
    # so we need a more bare bones approach.
    ldap_key = (ILDAPConfiguration, u"")
    if ldap_key not in sm._utility_registrations:
        logger.info("plone.app.ldap utility is already gone.")
    else:
        util = sm._utility_registrations[(ILDAPConfiguration, u"")][0]
        sm.unregisterUtility(component=util, provided=ILDAPConfiguration, name=u"")
        logger.info("Unregistered plone.app.ldap utility.")
    # It may still be in a helper dictionary.
    if ILDAPConfiguration in sm.utilities._provided:
        del sm.utilities._provided[ILDAPConfiguration]
        # _provided is a simple dictionary, not a persistent one,
        # so we need to signal explicitly that the utilies object has changed.
        sm.utilities._p_changed = True
        logger.info("Removed plone.app.ldap interface from utilities._provided.")

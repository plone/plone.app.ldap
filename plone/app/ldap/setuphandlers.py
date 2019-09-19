# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging


logger = logging.getLogger(__name__)


def uninstall(context):
    """Uninstall script"""
    PLUGIN_ID = "ldap-plugin"
    pas = getToolByName(context, 'acl_users')

    # Remove plugin if it exists.
    if PLUGIN_ID not in pas.objectIds():
        return
    pas._delObject(PLUGIN_ID)
    logger.info('Removed LDAP plugin %s from acl_users.', PLUGIN_ID)

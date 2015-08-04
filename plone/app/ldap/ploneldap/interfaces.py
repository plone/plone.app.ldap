# -*- coding: utf-8 -*-
from zope.interface import Interface


class IManagedLDAPPlugin(Interface):
    """Marker interface for the LDAP PAS plugin which is managed by us.
    """

# -*- coding: utf-8 -*-
from zope.browser.interfaces import IAdding


class IServerAdding(IAdding):
    """Marker interface for LDAP server add views.
    """


class IPropertyAdding(IAdding):
    """Marker interface for LDAP property add views.
    """

# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem
from zope.interface import implementer
from plone.app.ldap.engine.interfaces import ILDAPServer


@implementer(ILDAPServer)
class LDAPServer(SimpleItem):

    __name__ = None
    __parent__ = None

    def __init__(self, server=u"", connection_type=0, connection_timeout=5,
            operation_timeout=-1, enabled=False):
        self.server=server
        self.connection_type=connection_type
        self.connection_timeout=connection_timeout
        self.operation_timeout=operation_timeout
        self.enabled=enabled

    @property
    def port(self):
        if self.connection_type==0:
            return "389"
        elif self.connection_type==1:
            return "636"
        else:
            return "0"

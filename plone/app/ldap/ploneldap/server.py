# -*- coding: utf-8 -*-
from zope.component import adapter
from plone.app.ldap.engine.interfaces import ILDAPServer
from plone.app.ldap.ploneldap.util import guaranteePluginExists
from plone.app.ldap.ploneldap.util import getLDAPPlugin
from plone.app.ldap.ploneldap.util import configureLDAPServers
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.container.interfaces import IObjectRemovedEvent


def FindServerIndex(luf, server):
    servers=luf.getServers()

    for i in range(len(servers)):
        if servers[i].host==server.server and servers[i].port==server.port:
            return i
    raise KeyError


@adapter(ILDAPServer, IObjectCreatedEvent)
def HandleCreated(server, event):
    if guaranteePluginExists():
        # A new fully configured plugin has been created, so we do not
        # need to do anything anymore.
        return

    if not server.enabled:
        return

    luf=getLDAPPlugin()._getLDAPUserFolder()
    luf.manage_addServer(host=server.server,
                         port=server.port,
                         use_ssl=server.connection_type,
                         conn_timeout=server.connection_timeout,
                         op_timeout=server.operation_timeout)


@adapter(ILDAPServer, IObjectModifiedEvent)
def HandleModified(server, event):
    if guaranteePluginExists():
        # A new fully configured plugin has been created, so we do not
        # need to do anything anymore.
        return

    # We have no good way to determine which servers was edited, so just
    # reload them all
    configureLDAPServers()


@adapter(ILDAPServer, IObjectRemovedEvent)
def HandleRemoved(server, event):
    if guaranteePluginExists():
        # A new fully configured plugin has been created, so we do not
        # need to do anything anymore.
        return

    luf=getLDAPPlugin()._getLDAPUserFolder()
    servers=luf.getServers()

    for i in range(len(servers)):
        if servers[i]['host']==server.server and servers[i]['port']==server.port:
            luf.manage_deleteServers((i,))
            return

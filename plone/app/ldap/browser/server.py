# -*- coding: utf-8 -*-
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.ldap import LDAPMessageFactory as _
from plone.app.ldap.browser.baseform import Adding
from plone.app.ldap.browser.baseform import LDAPAddForm
from plone.app.ldap.browser.baseform import LDAPEditForm
from plone.app.ldap.browser.interfaces import IServerAdding
from plone.app.ldap.engine.interfaces import ILDAPConfiguration
from plone.app.ldap.engine.interfaces import ILDAPServerConfiguration
from plone.app.ldap.engine.server import LDAPServer
from zope.container.interfaces import INameChooser
from zope.component import adapts
from zope.component import getUtility
from zope.event import notify
from zope.formlib.form import FormFields
from zope.formlib.form import applyChanges
from zope.interface import implementer
from zope.lifecycleevent import ObjectCreatedEvent
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.traversing.interfaces import ITraversable


@implementer(IServerAdding)
class ServerAdding(Adding):

    def add(self, content):
        """Add the server to the context
        """
        storage = getUtility(ILDAPConfiguration).servers
        chooser = INameChooser(storage)
        storage[chooser.chooseName(None, content)] = content

    def namesAccepted(self):
        return False

    def nameAllowed(self):
        return False


class ServerAddForm(LDAPAddForm):
    """An add form for LDAP servers.
    """
    form_fields = FormFields(ILDAPServerConfiguration)
    label = _(u"Add Server")
    description = _(u"Add an new LDAP or ActiveDirectory server.")
    form_name = _(u"Configure server")
    fieldset = "servers"

    def create(self, data):
        server = LDAPServer()
        applyChanges(server, self.form_fields, data)
        notify(ObjectCreatedEvent(server))
        return server


class ServerEditForm(LDAPEditForm):
    """An edit form for LDAP servers.
    """
    form_fields = FormFields(ILDAPServerConfiguration)
    label = _(u"Edit Server")
    description = _(u"Edit a LDAP or ActiveDirectory server.")
    form_name = _(u"Configure server")
    fieldset = "servers"


@implementer(ITraversable)
class ServerNamespace(object):
    """LDAP server traversing.

    Traversing to portal/++ldapserver++id will traverse to the ldap server and
    return it in the current context, acquisition-wrapped.
    """
    adapts(ISiteRoot, IBrowserRequest)

    def __init__(self, context, request=None):
        self.context=context
        self.request=request

    def traverse(self, name, ignore):
        storage = getUtility(ILDAPConfiguration).servers
        return storage[name].__of__(self.context)

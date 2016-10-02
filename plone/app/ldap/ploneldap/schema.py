# -*- coding: utf-8 -*-
from zope.component import adapter
from plone.app.ldap.engine.interfaces import ILDAPProperty
from plone.app.ldap.ploneldap.util import guaranteePluginExists
from plone.app.ldap.ploneldap.util import getLDAPPlugin
from plone.app.ldap.ploneldap.util import configureLDAPSchema
from plone.app.ldap.ploneldap.util import addMandatorySchemaItems
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.container.interfaces import IObjectRemovedEvent


@adapter(ILDAPProperty, IObjectCreatedEvent)
def HandleCreated(property, event):
    if guaranteePluginExists():
        # A new fully configured plugin has been created, so we do not
        # need to do anything anymore.
        return

    luf=getLDAPPlugin()._getLDAPUserFolder()
    # In case if the user is adding a property which is already present in the
    # backend since it is obligatory we try to delete it first.
    luf.manage_deleteLDAPSchemaItems([str(property.ldap_name)])

    luf.manage_addLDAPSchemaItem(
            ldap_name=str(property.ldap_name),
            friendly_name=property.description,
            public_name=str(property.plone_name),
            multivalued=property.multi_valued,
            binary=property.binary)


@adapter(ILDAPProperty, IObjectModifiedEvent)
def HandleModified(property, event):
    if guaranteePluginExists():
        # A new fully configured plugin has been created, so we do not
        # need to do anything anymore.
        return

    configureLDAPSchema()


@adapter(ILDAPProperty, IObjectRemovedEvent)
def HandleRemoved(property, event):
    if guaranteePluginExists():
        # A new fully configured plugin has been created, so we do not
        # need to do anything anymore.
        return

    luf=getLDAPPlugin()._getLDAPUserFolder()
    luf.manage_deleteLDAPSchemaItems([str(property.ldap_name)])

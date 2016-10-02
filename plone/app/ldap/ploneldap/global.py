# -*- coding: utf-8 -*-
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from plone.app.ldap.engine.interfaces import ILDAPBinding
from plone.app.ldap.ploneldap.util import guaranteePluginExists
from plone.app.ldap.ploneldap.util import getLDAPPlugin


@adapter(ILDAPBinding, IObjectModifiedEvent)
def HandleModified(config, event):
    if guaranteePluginExists():
        # A new fully configured plugin has been created, so we do not
        # need to do anything anymore.
        return

    luf=getLDAPPlugin()._getLDAPUserFolder()
    luf.manage_edit(
            title="Plone managed LDAP",
            login_attr=str(config.schema[config.login_attribute].ldap_name),
            uid_attr=str(config.schema[config.userid_attribute].ldap_name),
            rdn_attr=str(config.schema[config.rdn_attribute].ldap_name),
            users_base=config.user_base or "",
            users_scope=config.user_scope,
            groups_base=config.group_base or "",
            groups_scope=config.group_scope,
            binduid=str(config.bind_dn) or "",
            bindpwd=str(config.bind_password) or "",
            encryption=config.password_encryption,
            roles=config.default_user_roles or "",
            read_only=config.read_only,
            obj_classes=config.user_object_classes)

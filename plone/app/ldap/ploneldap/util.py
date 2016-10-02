# -*- coding: utf-8 -*-
from zope.component.hooks import getSite
from zope.component import getUtility
from zope.interface import directlyProvides
from plone.app.ldap.engine.interfaces import ILDAPConfiguration
from plone.app.ldap.engine.schema import LDAPProperty
from Products.CMFCore.utils import getToolByName
from Products.PloneLDAP.plugins.ad import PloneActiveDirectoryMultiPlugin
from Products.PloneLDAP.plugins.ldap import PloneLDAPMultiPlugin
from Products.PloneLDAP.factory import genericPluginCreation
from plone.app.ldap.ploneldap.interfaces import IManagedLDAPPlugin


def getPAS():
    site=getSite()
    return getToolByName(site, "acl_users")


def guaranteePluginExists():
    """Make sure a proper PAS plugin exists.

    If a plugin exists but it is of the wrong type (AD vs standard LDAP)
    the plugin is removed and a new one is created.

    If a new plugin has been created True is returned. If there was
    a valid plugin present False is returned.
    """
    config=getUtility(ILDAPConfiguration)
    try:
        plugin=getLDAPPlugin()
        if plugin.meta_type==PloneActiveDirectoryMultiPlugin.meta_type and \
                config.ldap_type==u"AD":
            return False
        if plugin.meta_type==PloneLDAPMultiPlugin.meta_type and \
                config.ldap_type==u"LDAP":
            return False

        # There is a managed plugin, but it is of the wrong type.
        pas=getPAS()
        pas.manage_delObjects([plugin.getId()])
    except KeyError:
        pass

    createLDAPPlugin()
    configureLDAPServers()
    configureLDAPSchema()
    return True


def getLDAPPlugin():
    pas=getPAS()
    for plugin in pas.objectValues([PloneActiveDirectoryMultiPlugin.meta_type,
                                    PloneLDAPMultiPlugin.meta_type]):
        if IManagedLDAPPlugin.providedBy(plugin):
            return plugin

    raise KeyError


def createLDAPPlugin(id="ldap-plugin"):
    pas=getPAS()
    config=getUtility(ILDAPConfiguration)
    if config.ldap_type==u"AD":
        klass=PloneActiveDirectoryMultiPlugin
    else:
        klass=PloneLDAPMultiPlugin

    genericPluginCreation(pas, klass,
            id=id,
            title="Plone managed LDAP",
            login_attr=str(config.schema[config.login_attribute].ldap_name),
            uid_attr=str(config.schema[config.userid_attribute].ldap_name),
            rdn_attr=str(config.schema[config.rdn_attribute].ldap_name),
            users_base=config.user_base or "",
            users_scope=config.user_scope,
            groups_base=config.group_base or "",
            groups_scope=config.group_scope,
            binduid=config.bind_dn or "",
            bindpwd=config.bind_password or "",
            encryption=config.password_encryption,
            roles=config.default_user_roles or "",
            local_groups=config.local_groups,
            read_only=config.read_only,
            obj_classes=config.user_object_classes)

    plugin=getattr(pas, id)
    plugin.groupid_attr="cn"
    directlyProvides(plugin, IManagedLDAPPlugin)
    enablePASInterfaces()
    enableCaching(config.cache)
    luf=plugin._getLDAPUserFolder()
    luf.manage_changeProperty('_extra_user_filter', config.extra_user_filter)
    luf.manage_changeProperty('_implicit_mapping', config.implicit_mapping)
    luf.manage_changeProperty('_groups_mappings', config.group_mappings)


def configureLDAPServers():
    luf=getLDAPPlugin()._getLDAPUserFolder()
    config=getUtility(ILDAPConfiguration)

    luf.manage_deleteServers(range(len(luf.getServers())))
    for server in config.servers.values():
        if server.enabled:
            luf.manage_addServer(host=server.server,
                                 port=server.port,
                                 use_ssl=server.connection_type,
                                 conn_timeout=server.connection_timeout,
                                 op_timeout=server.operation_timeout)


def addMandatorySchemaItems():
    config=getUtility(ILDAPConfiguration)

    if config.ldap_type==u"AD":
        required = [("dn", {'description': "Distinguished Name"}),
                    ("objectGUID", {'description': "AD Object GUID",
                            'multi_valued': False, 'binary': True}),
                    ("cn", {'description': "Canonical Name"}),
                    ("sAMAccountName", {'description': "AD User Name"}),
                    ("memberOf", {'description': "Group DNs",
                            'multi_valued': True, 'plone_name': "memberOf"})]
    else:
        required = []

    for attr, args in required:
        if attr not in config.schema:
            config.schema.addItem(LDAPProperty(ldap_name=attr, **args))
        if attr not in config.required_attributes:
            config.required_attributes.append(attr)


def configureLDAPSchema():
    luf=getLDAPPlugin()._getLDAPUserFolder()
    config=getUtility(ILDAPConfiguration)
    addMandatorySchemaItems()

    schema={}
    for property in config.schema.values():
        schema[str(property.ldap_name)]=dict(
                ldap_name=str(property.ldap_name),
                friendly_name=property.description,
                public_name=str(property.plone_name),
                multivalued=property.multi_valued,
                binary=property.binary)
    luf.setSchemaConfig(schema)


def enablePASInterfaces():
    plugin=getLDAPPlugin()
    config=getUtility(ILDAPConfiguration)

    common_interfaces = [
            'IUserEnumerationPlugin',
            'IGroupsPlugin',
            'IGroupEnumerationPlugin',
            'IRoleEnumerationPlugin',
            'IAuthenticationPlugin',
            'ICredentialsResetPlugin',
            'IPropertiesPlugin',
            'IRolesPlugin',
            'IGroupIntrospection',
            ]

    ldap_interfaces = common_interfaces + [
            'IGroupManagement',
            'IUserAdderPlugin',
            'IUserManagement',
            ]

    ad_interfaces = common_interfaces

    if config.activated_plugins:
        plugin.manage_activateInterfaces(config.activated_plugins)
    else:
        if config.ldap_type==u"AD":
            plugin.manage_activateInterfaces(ad_interfaces)
            config.activated_plugins = ad_interfaces
        else:
            plugin.manage_activateInterfaces(ldap_interfaces)
            config.activated_plugins = ldap_interfaces

    plugins=getPAS().plugins
    if "IPropertiesPlugin" in config.activated_plugins:
        iface=plugins._getInterfaceFromName("IPropertiesPlugin")
        for i in range(len(plugins.listPlugins(iface))-1):
            plugins.movePluginsUp(iface, [plugin.getId()])

    if config.ldap_type != u"AD":
        for p in ("IUserAdderPlugin", "IGroupManagement"):
            if p in config.activated_plugins:
                iface=plugins._getInterfaceFromName(p)
                for i in range(len(plugins.listPlugins(iface))-1):
                    plugins.movePluginsUp(iface, [plugin.getId()])



def enableCaching(cache_manager="RAMCache"):
    pas=getPAS()
    if pas.ZCacheable_getManager() is None:
        pas.ZCacheable_setManagerId(manager_id=cache_manager)
    getLDAPPlugin().ZCacheable_setManagerId(manager_id=cache_manager)

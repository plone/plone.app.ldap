# -*- coding: utf-8 -*-
from plone.app.ldap.engine.interfaces import ILDAPConfiguration
from plone.app.ldap.engine.schema import LDAPProperty
from plone.app.ldap.engine.server import LDAPServer
from plone.app.ldap.engine.storage import LDAPSchema
from plone.app.ldap.engine.storage import LDAPServerStorage
from plone.app.ldap.ploneldap.util import configureLDAPSchema
from plone.app.ldap.ploneldap.util import configureLDAPServers
from plone.app.ldap.ploneldap.util import createLDAPPlugin
from plone.app.ldap.ploneldap.util import getLDAPPlugin
from plone.app.ldap.ploneldap.util import getPAS
from six import StringIO
from xml.dom.minidom import parseString
from zope.component import getUtility
from zope.pagetemplate.pagetemplatefile import PageTemplateFile

import ast
import logging


ldap_props = ['_login_attr',
              '_uid_attr',
              '_rdnattr',
              'users_base',
              'users_scope',
              '_local_groups',
              '_implicit_mapping',
              '_groups_mappings',
              'groups_base',
              'groups_scope',
              '_binduid',
              '_bindpwd',
              '_binduid_usage',
              'read_only',
              '_user_objclasses',
              '_extra_user_filter',
              '_pwd_encryption',
              '_roles']

_FILENAME = 'ldap_plugin.xml'

update = True


class LDAPPluginExportImport:
    """In- and Exporter for LDAP-PAS-Plugin
    """

    def exportData(self, context, out):
        template = PageTemplateFile('xml/%s' % _FILENAME, globals())  # .__of__(context.getSite())
        info = self._getExportInfo(context)
        if info:
            context.writeDataFile('%s' % _FILENAME, template(info=info).encode('utf-8'), 'text/xml')
            print >> out, "GenericSetup Configuration for ldap exported"

    def getTypeStr(self, value):
        val_type = 'str'
        if isinstance(value, list):
            val_type = 'list'
        # check for bool before int as a bool is also an instance of int
        elif isinstance(value, bool):
            val_type = 'bool'
        elif isinstance(value, int):
            val_type = 'int'
        return val_type

    def _getExportInfo(self, context):
        info = []
        portal = context.getSite()
        mt = getattr(portal, 'acl_users')
        for obj in mt.objectValues():
            if obj.meta_type in ['Plone LDAP plugin', 'LDAP Multi Plugin', 'Plone Active Directory plugin', 'ActiveDirectory Multi Plugin']:
                interfaces = []
                for p_info in obj.plugins.listPluginTypeInfo():
                    interface = p_info['interface']
                    actives = obj.plugins.listPlugins(interface)
                    act_ids = [x[0] for x in actives]
                    if obj.getId() in act_ids:
                        interfaces.append(p_info['id'])

                plugin_props = obj.propertyMap()
                for prop in plugin_props:
                    value = obj.getProperty(prop['id'])
                    if prop['type'] in ['string', 'int']:
                        prop['value'] = obj.getProperty(prop['id'])
                plugin_props = [i for i in plugin_props if 'value' in i.keys()]

                c_info = {
                    'meta_type': obj.meta_type,
                    'plugin_props': plugin_props,
                    'interfaces': interfaces,
                    'properties': [],
                    'schema': [],
                    'servers': [],
                    'id': obj.getId(),
                    'title': obj.title}
                uf = getattr(obj, 'acl_users')
                for prop in ldap_props:
                    value = uf.getProperty(prop)
                    val_type = self.getTypeStr(value)
                    if val_type != 'list':
                        value = [value]
                    c_info['properties'].append({'id': prop, 'type': val_type, 'value': value})
                for server in uf.getServers():
                    c_server = {'content': []}
                    for key in server.keys():
                        c_server['content'].append({'id': key, 'value': server[key], 'type': self.getTypeStr(server[key])})
                    c_info['servers'].append(c_server)
                schema = uf.getSchemaConfig()
                for key in schema.keys():
                    a_item = {'id': key, 'content': []}
                    for subkey in schema[key]:
                        s_item = {'id': subkey, 'value': schema[key][subkey], 'type': self.getTypeStr(schema[key][subkey])}
                        a_item['content'].append(s_item)
                    c_info['schema'].append(a_item)
                info.append(c_info)

        return info

    def importData(self, context, out):
        logger = context.getLogger('ldapsettings')
        xml = context.readDataFile(_FILENAME)
        if xml is None:
            logger.info('Nothing to import.')
            return

        portal = context.getSite()
        pas = getattr(portal, 'acl_users')
        dom = parseString(xml)
        root = dom.documentElement

        for plugin in root.getElementsByTagName('ldapplugin'):
            self.extractData(plugin, pas, out)

    def extractData(self, root, pas, out):
        plug_id = str(root.getAttribute('id'))
        update = root.getAttribute('update') == 'True'
        meta_type = root.getAttribute('meta_type')

        settings = {}
        interfaces = []
        plugin_props = []
        for prop in root.getElementsByTagName('plugin_property'):
            p_type = prop.getAttribute('type')
            p_id = prop.getAttribute('id')
            value = prop.getAttribute('value')
            if p_type == 'int':
                value = int(value)
            if p_type == 'string':
                value = str(value)
            plugin_props.append({'id': p_id, 'type': p_type, 'value': value})

        for iface in root.getElementsByTagName('interface'):
            interfaces.append(iface.getAttribute('value'))

        caches = list()
        for node in root.getElementsByTagName('cache'):
            caches.append(node.getAttribute('value'))

        if len(caches) > 1:
            raise ValueError('You can not define multiple <cache> properties')

        cache = ''
        if len(caches):
            cache = caches[0]

        for prop in root.getElementsByTagName('property'):
            type = prop.getAttribute('type')
            values = []
            for v in prop.getElementsByTagName('item'):
                values.append(v.getAttribute('value'))
            id = prop.getAttribute('id')
            if type == 'list':
                # values are unicode strings
                # _user_objclasses and _roles need to be strings
                if id in ['_user_objclasses', '_roles']:
                    value = [item.encode('utf8') for item in values]
                else:
                    value = values
            else:
                value = values[0]
            if type == 'int':
                value = int(value)
            if type == 'bool':
                value = (value.lower() != 'false' and 1 or 0)
            settings[id] = value
        schema = {}
        for schemanode in root.getElementsByTagName('schema'):
            for attr in schemanode.getElementsByTagName('attr'):
                c_id = attr.getAttribute('id')
                c_attr = {}
                for item in attr.getElementsByTagName('item'):
                    if item.getAttribute('value') != 'False':
                        c_attr[str(item.getAttribute('id'))] = str(item.getAttribute('value'))
                    else:
                        c_attr[str(item.getAttribute('id'))] = False
                schema[str(c_id)] = c_attr
        servers = []
        for server in root.getElementsByTagName('server'):
            c_server = {'update': (server.getAttribute('update') == 'True'),
                        'delete': (server.getAttribute('delete') == 'True')}
            for item in server.getElementsByTagName('item'):
                value = item.getAttribute('value')
                type = item.getAttribute('type')
                id = item.getAttribute('id')
                if type == 'int':
                    value = int(value)
                c_server[id] = value
            servers.append(c_server)

        # always update if it doesn't exist
        if plug_id not in pas.objectIds():
            update = True

        if update:
            # delete existing LDAP plug-in
            if plug_id in pas.objectIds():
                try:
                    plugin = getLDAPPlugin()
                    pas = getPAS()
                    pas.manage_delObjects([plugin.getId()])
                except KeyError:
                    # pass
                    """
                    There are two reasons to not pass here. First, if we pass
                    and go to recreate later and both plugins have the same it, it
                    will error out for the id already existing. Second, if they
                    don't have the same id but have the same settings, they will then
                    in practice (if its set up correct) have duplicate users, which
                    will subsequently break any group or role lookups which assert
                    on the duplicate users. I don't see any tests on this so if there
                    is an argument to leave this as a pass let me know.
                    """
                    logging.error("There is an ldap multi plugin in your "+
                        "system (%s) that is not managed "%plug_id +
                        "by this generic setup script. To have everything "+
                        "managed by GS, please delete and " +
                        "reinstall or set update=False in your ldap_plugin.xml"+
                        " root.")
                    logging.error("Installing LDAP Plugin with GS failed")
                    return

            # base configuration
            config = getUtility(ILDAPConfiguration)
            if meta_type in [u"Plone Active Directory plugin",
                             u"ActiveDirectory Multi Plugin"]:
                config.ldap_type = u"AD"
            else:
                config.ldap_type = u"LDAP"

            config.login_attribute = settings['_login_attr']
            config.userid_attribute = settings['_uid_attr']
            config.rdn_attribute = settings['_rdnattr']
            config.user_base = settings['users_base']
            config.user_scope = settings['users_scope']
            config.group_base = settings['groups_base']
            config.group_scope = settings['groups_scope']
            config.bind_dn = settings['_binduid']
            config.bind_password = settings['_bindpwd']
            config.user_object_classes = ','.join(settings['_user_objclasses'])
            config.extra_user_filter = settings['_extra_user_filter']
            config.password_encryption = settings['_pwd_encryption']
            config.default_user_roles = ','.join(settings['_roles'])
            config.implicit_mapping = settings['_implicit_mapping']
            config.local_groups = settings['_local_groups']
            try:
                config.group_mappings = ast.literal_eval(settings['_groups_mappings'])
            except (ValueError, SyntaxError, KeyError):
                config.group_mappings = {}
            config.read_only = settings['read_only']
            config.activated_plugins = interfaces
            config.cache = cache

            # servers
            config.servers = LDAPServerStorage()
            for server in servers:
                obj = LDAPServer(server=server['host'],
                                 connection_type=(server['protocol'] == 'ldaps'),
                                 connection_timeout=server['conn_timeout'],
                                 operation_timeout=server['op_timeout'],
                                 enabled=True)
                config.servers.addItem(obj)

            # schema
            config.schema = LDAPSchema()
            for property in schema.itervalues():
                obj = LDAPProperty(ldap_name=property.get('ldap_name', ''),
                                   plone_name=property.get('public_name', ''),
                                   description=property.get('friendly_name', ''),
                                   multi_valued=property.get('multivalued', False),
                                   binary=property.get('binary', False))
                config.schema.addItem(obj)
            # recreate new LDAP plug-in
            createLDAPPlugin(plug_id)
            configureLDAPServers()
            configureLDAPSchema()


def exportLDAPSettings(context):
    exporter = LDAPPluginExportImport()
    out = StringIO()
    exporter.exportData(context, out)
    logger = context.getLogger('ldapsettings')
    logger.info(out.getvalue())


def importLDAPSettings(context):
    importer = LDAPPluginExportImport()
    out = StringIO()
    importer.importData(context, out)
    logger = context.getLogger('ldapsettings')
    logger.info(out.getvalue())

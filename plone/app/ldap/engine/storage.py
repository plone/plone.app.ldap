# -*- coding: utf-8 -*-
from zope.interface import implementer
from zope.container.ordered import OrderedContainer
from zope.container.interfaces import INameChooser
from plone.app.ldap.engine.interfaces import ILDAPServerStorage
from plone.app.ldap.engine.interfaces import ILDAPSchema
from plone.app.ldap.engine.interfaces import ILDAPConfiguration
from BTrees.OOBTree import OOBTree
from ldap import SCOPE_SUBTREE
from plone.app.ldap.engine.schema import LDAPProperty


@implementer(ILDAPConfiguration)
class LDAPConfiguration(OrderedContainer):

    ldap_type = u"LDAP"
    rdn_attribute = "uid"
    userid_attribute = "uid"
    login_attribute = "uid"
    required_attributes = []

    user_object_classes = "pilotPerson"

    bind_dn = ""
    bind_password = ""
    user_base = ""
    user_scope = SCOPE_SUBTREE
    group_base = ""
    group_scope = SCOPE_SUBTREE
    password_encryption = "crypt"
    default_user_roles = "Member"
    extra_user_filter = ""
    local_groups = False
    implicit_mapping = False
    group_mappings = {}
    read_only = False
    activated_plugins = []
    cache = ''

    def __init__(self):
        self.servers=LDAPServerStorage()
        self.schema=LDAPSchema()

        self.schema.addItem(LDAPProperty(
            ldap_name="uid", description=u"User id"))
        self.schema.addItem(LDAPProperty(
            ldap_name="mail", plone_name="email",
            description=u"Email address"))
        self.schema.addItem(LDAPProperty(
            ldap_name="cn", plone_name="fullname",
            description=u"Canonical Name"))
        self.schema.addItem(LDAPProperty(
            ldap_name="sn", description=u"Surname (unused)"))


class LDAPContainer(OrderedContainer):
    """Base class for our containers.
    """
    def __init__(self):
        OrderedContainer.__init__(self)
        self._data=OOBTree()

    def addItem(self, item):
        chooser=INameChooser(self)
        item_id = getattr(item, 'ldap_name', None) or chooser.chooseName(None, item)
        self[item_id]=item


@implementer(ILDAPServerStorage)
class LDAPServerStorage(LDAPContainer):
    """A container for LDAP servers.
    """


@implementer(ILDAPSchema)
class LDAPSchema(LDAPContainer):
    """A container for LDAP properties.
    """

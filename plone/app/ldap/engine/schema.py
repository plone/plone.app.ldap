# -*- coding: utf-8 -*-
from OFS.SimpleItem import SimpleItem
from zope.interface import implementer
from plone.app.ldap.engine.interfaces import ILDAPProperty


@implementer(ILDAPProperty)
class LDAPProperty(SimpleItem):

    __name__ = None
    __parent__ = None

    def __init__(self, ldap_name=u"", plone_name=u"", description=u"",
                 multi_valued=False, binary=False):
        self.description=description
        self.ldap_name=ldap_name
        self.plone_name=plone_name
        self.multi_valued=multi_valued
        self.binary=binary

    def __setattr__(self, name, value):
        if name in ('ldap_name', 'plone_name', 'description'):
            # Store blank fields as empty strings to avoid exporting a
            # literal 'None' with e.g. str(property.attr).
            value = value or u""
        super(LDAPProperty, self).__setattr__(name, value)

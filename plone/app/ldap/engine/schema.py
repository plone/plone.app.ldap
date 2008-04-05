from OFS.SimpleItem import SimpleItem
from zope.interface import implements
from plone.app.ldap.engine.interfaces import ILDAPProperty

class LDAPProperty(SimpleItem):
    implements(ILDAPProperty)

    __name__ = None
    __parent__ = None

    def __init__(self, ldap_name=u"", plone_name=u"", description=u"",
                 multi_valued=False):
        self.description=description
        self.ldap_name=ldap_name
        self.plone_name=plone_name
        self.multi_valued=multi_valued


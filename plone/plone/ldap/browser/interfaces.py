from zope.app.container.interfaces import IAdding


class IServerAdding(IAdding):
    """Marker interface for LDAP server add views.
    """


class IPropertyAdding(IAdding):
    """Marker interface for LDAP property add views.
    """

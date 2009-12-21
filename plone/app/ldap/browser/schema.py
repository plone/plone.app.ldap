from Acquisition import aq_inner
from Acquisition import Implicit
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.formlib.form import FormFields
from zope.formlib.form import applyChanges
from Products.Five import BrowserView
from Products.CMFCore.interfaces import ISiteRoot
from plone.app.ldap import LDAPMessageFactory as _
from plone.app.ldap.browser.interfaces import IPropertyAdding
from plone.app.ldap.engine.interfaces import ILDAPConfiguration
from plone.app.ldap.engine.interfaces import ILDAPPropertyConfiguration
from plone.app.ldap.engine.schema import LDAPProperty
from plone.app.ldap.browser.baseform import LDAPAddForm
from plone.app.ldap.browser.baseform import LDAPEditForm
from plone.app.ldap.browser.baseform import Adding


class PropertyAdding(Adding):
    implements(IPropertyAdding)

    def add(self, content):
        """Add the property to the schema
        """
        schema=getUtility(ILDAPConfiguration).schema
        schema.addItem(content)

    def namesAccepted(self):
        return False

    def nameAllowed(self):
        return False


class PropertyAddForm(LDAPAddForm):
    """An add form for LDAP properties.
    """
    form_fields = FormFields(ILDAPPropertyConfiguration)
    label = _(u"Add Property")
    description = _(u"Add a LDAP property to the schema.")
    form_name = _(u"Configure property")
    fieldset = "schema"

    def create(self, data):
        property = LDAPProperty()
        applyChanges(property, self.form_fields, data)
        return property


class PropertyEditForm(LDAPEditForm):
    """An edit form for LDAP properties.
    """
    form_fields = FormFields(ILDAPPropertyConfiguration)
    label = _(u"Edit Property")
    description = _(u"Edit a LDAP property.")
    form_name = _(u"Configure property")
    fieldset = "schema"


class SchemaNamespace(object):
    """LDAP schema traversing.
    """
    implements(ITraversable)
    adapts(ISiteRoot, IBrowserRequest)

    def __init__(self, context, request=None):
        self.context=context
        self.request=request


    def traverse(self, name, ignore):
        schema = getUtility(ILDAPConfiguration).schema
        return schema[name].__of__(self.context)



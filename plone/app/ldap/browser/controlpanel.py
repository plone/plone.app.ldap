from ldap import LDAPError
import logging
from zope.lifecycleevent import ObjectModifiedEvent
from zope.formlib.form import haveInputWidgets
from zope.formlib.form import applyChanges
from zope.formlib.form import action
from zope.formlib.form import FormFields
from zope.event import notify
from zope.component import getUtility
from plone.app.ldap.engine.interfaces import ILDAPConfiguration
from plone.app.ldap.engine.interfaces import ILDAPBinding
from plone.memoize.instance import memoize
from Products.Five.formlib.formbase import EditForm
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from zope.schema.interfaces import ValidationError
from zope.app.form.interfaces import WidgetInputError

class LDAPBindFailure(ValidationError):
    __doc__ = _(u"LDAP server refused your credentials")


logger = logging.getLogger("plone.app.ldap")

def LDAPBindingFactory(context):
    return getUtility(ILDAPConfiguration)


class LDAPControlPanel(EditForm):
    template = ViewPageTemplateFile("controlpanel.pt")

    form_fields = FormFields(ILDAPBinding)
    label = u"LDAP Control Panel"
    description = u"XXXXX"
    form_name = u"LDAP Control Panel form name"


    @action(_("Apply"), condition=haveInputWidgets)
    def handle_edit_actions(self, action, data):
        # Filter out non-required fields that have no value so their
        # existing value is not overwritten. This protects us from
        # overwriting the bind password.
        data = dict([(key,value) for (key,value) in data.iteritems() 
                        if value is not None])
        if applyChanges(self.context, self.form_fields, data, self.adapters):
            try:
                notify(ObjectModifiedEvent(self.storage))
            except LDAPError, e:
                widget=self.widgets.get("bind_dn")

                widget.error=WidgetInputError("bind_dn", widget.label,
                        LDAPBindFailure("value"))
                self.errors += (widget.error,)
                self.status= _("There were errors")
                return


    @property
    @memoize
    def storage(self):
        return getUtility(ILDAPConfiguration)


    def update(self):
        form = self.request.form

        storage=self.storage
        propertyIds=form.get("propertyId", [])
        schema=storage.schema
        serverIds=form.get("serverId", [])
        servers=storage.servers

        if form.get("form.button.DeleteProperty", None) is not None:
            for id in propertyIds:
                if id in schema:
                    del schema[id]
        elif form.get("form.button.EnableServer", None) is not None:
            for id in serverIds:
                if id in servers:
                    servers[id].enabled=True
        elif form.get("form.button.DisableServer", None) is not None:
            for id in serverIds:
                if id in servers:
                    servers[id].enabled=False
        elif form.get("form.button.DeleteServer", None) is not None:
            for id in serverIds:
                if id in servers:
                    del servers[id]

        return EditForm.update(self)


    def servers(self):
        def contype(c):
            if c==0:
                return "LDAP"
            elif c==1:
                return "LDAP over SSL"
            else:
                return "LDAP over IPC"

        return [ dict(id=s.__name__,
                      enabled=s.enabled,
                      server=s.server,
                      connection_type=contype(s.connection_type),
                      connection_timeout=s.connection_timeout,
                      operation_timeout=s.operation_timeout)
                 for s in self.storage.servers.values() ]


    def schema(self):
        storage=self.storage

        def protected(attr):
            return attr.__name__ in (storage.rdn_attribute,
                                     storage.userid_attribute,
                                     storage.login_attribute)

        return [ dict(id=p.__name__,
                      description=p.description,
                      ldap_name=p.ldap_name,
                      plone_name=p.plone_name,
                      multi_valued=p.multi_valued,
                      protected=protected(p))
                 for p in storage.schema.values() ]



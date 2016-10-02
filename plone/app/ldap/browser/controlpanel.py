# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from five.formlib.formbase import EditForm
from ldap import LDAPError
from plone.app.ldap import LDAPMessageFactory as _
from plone.app.ldap.engine.interfaces import ILDAPBinding
from plone.app.ldap.engine.interfaces import ILDAPConfiguration
from plone.app.ldap.ploneldap.util import getLDAPPlugin
from plone.memoize.instance import memoize
from zope.formlib.interfaces import WidgetInputError
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.event import notify
from zope.formlib.form import FormFields
from zope.formlib.form import action
from zope.formlib.form import applyChanges
from zope.formlib.form import haveInputWidgets
from zope.lifecycleevent import ObjectModifiedEvent
from zope.schema.interfaces import ValidationError
import logging

try:
    from zope.lifecycleevent import ObjectRemovedEvent
    ObjectRemovedEvent  # pyflakes
except:
    from zope.container.contained import ObjectRemovedEvent


class LDAPBindFailure(ValidationError):
    __doc__ = _(u"LDAP server refused your credentials")


logger = logging.getLogger("plone.app.ldap")


def LDAPBindingFactory(context):
    return getUtility(ILDAPConfiguration)


class LDAPControlPanel(EditForm):
    template = ViewPageTemplateFile("controlpanel.pt")

    form_fields = FormFields(ILDAPBinding)
    label = u"LDAP Control Panel"
    description = u"In this control panel you can configure an LDAP connection. You can either use a standard LDAP server or a Microsoft Active Directory Server."
    form_name = u"LDAP Control Panel"

    @action(_("Apply"), condition=haveInputWidgets)
    def handle_edit_actions(self, action, data):
        # Filter out non-required fields that have no value so their
        # existing value is not overwritten. This protects us from
        # overwriting the bind password.
        data = dict([(key, value) for (key, value) in data.iteritems()
                     if value is not None])
        if applyChanges(self.context, self.form_fields, data, self.adapters):
            try:
                notify(ObjectModifiedEvent(self.storage))
            except LDAPError:
                widget=self.widgets.get("bind_dn")

                widget.error=WidgetInputError("bind_dn", widget.label,
                                              LDAPBindFailure("value"))
                self.errors += (widget.error,)
                self.status= _("There were errors")
        return self.request.response.redirect(self.nextURL())

    @action(_(u'label_enable', default=u'Enable'), name=u'EnableServer')
    def handle_enable_server(self, action, data):
        for id in self.request.form.get("serverId", []):
            if id in self.storage.servers:
                server = self.storage.servers[id]
                if server.enabled is False:
                    server.enabled = True
                    notify(ObjectModifiedEvent(server))
        return self.request.response.redirect(self.nextURL())

    @action(_(u'label_disable', default=u'Disable'), name=u'DisableServer')
    def handle_disable_server(self, action, data):
        for id in self.request.form.get("serverId", []):
            if id in self.storage.servers:
                server = self.storage.servers[id]
                if server.enabled is True:
                    server.enabled = False
                    notify(ObjectModifiedEvent(server))
        return self.request.response.redirect(self.nextURL())

    @action(_(u'label_delete', default=u'Delete'), name=u'DeleteServer')
    def handle_delete_server(self, action, data):
        for id in self.request.form.get("serverId", []):
            if id in self.storage.servers:
                notify(ObjectRemovedEvent(self.storage.servers[id]))
                del self.storage.servers[id]
        return self.request.response.redirect(self.nextURL())

    @action(_(u'label_delete_property', default=u'Delete'), name=u'DeleteProperty')
    def handle_delete_property(self, action, data):
        for id in self.request.form.get("propertyId", []):
            if id in self.storage.schema:
                notify(ObjectRemovedEvent(self.storage.schema[id]))
                del self.storage.schema[id]
        return self.request.response.redirect(self.nextURL())

    @action(_(u'label_purge', default=u'Purge'), name=u'Purge')
    def handle_cache_purge(self, action, data):
        luf = getLDAPPlugin()._getLDAPUserFolder()
        luf.manage_reinit()
        self.status = 'User caches cleared'
        return self.request.response.redirect(self.nextURL())

    @action(_(u'label_update_cache_timeouts', default=u'Update Cache Timeouts'), name=u'UpdateCacheTimeouts')
    def handle_update_cache_timeouts(self, action, data):
        luf = getLDAPPlugin()._getLDAPUserFolder()
        for cache_type, cache_value_name in [
                ('authenticated', 'auth_cache_seconds'),
                ('anonymous', 'anon_cache_seconds'),
                ('negative', 'negative_cache_seconds'), ]:
            cache_value = self.request.form['form.' + cache_value_name]
            try:
                cache_value = int(cache_value)
            except ValueError:
                continue
            if cache_value != getattr(self, cache_value_name, None):
                luf.setCacheTimeout(cache_type=cache_type, timeout=cache_value)
                self.status = 'Cache timeout changed'
        return self.request.response.redirect(self.nextURL())

    # cache properties delegate to the LDAPUserFolder instance
    def get_auth_cache_seconds(self):
        try:
            luf = getLDAPPlugin()._getLDAPUserFolder()
        except KeyError:
            return 600
        return luf.getCacheTimeout('authenticated')
    def set_auth_cache_seconds(self, value):
        luf = getLDAPPlugin()._getLDAPUserFolder()
        luf.setCacheTimeout(cache_type='authenticated', timeout=value)
    auth_cache_seconds = property(get_auth_cache_seconds, set_auth_cache_seconds)

    def get_anon_cache_seconds(self):
        try:
            luf = getLDAPPlugin()._getLDAPUserFolder()
        except KeyError:
            return 600
        return luf.getCacheTimeout('anonymous')
    def set_anon_cache_seconds(self, value):
        luf = getLDAPPlugin()._getLDAPUserFolder()
        luf.setCacheTimeout(cache_type='anonymous', timeout=value)
    anon_cache_seconds = property(get_anon_cache_seconds, set_anon_cache_seconds)

    def get_negative_cache_seconds(self):
        try:
            luf = getLDAPPlugin()._getLDAPUserFolder()
        except KeyError:
            return 600
        return luf.getCacheTimeout('negative')
    def set_negative_cache_seconds(self, value):
        luf = getLDAPPlugin()._getLDAPUserFolder()
        luf.setCacheTimeout(cache_type='negative', timeout=value)
    negative_cache_seconds = property(get_negative_cache_seconds, set_negative_cache_seconds)

    def anon_cache(self):
        try:
            luf = getLDAPPlugin()._getLDAPUserFolder()
        except KeyError:
            return []
        users = luf.getUsers(authenticated=0)
        for user in users:
            user.cache_type = 'anonymous'
        return users

    def auth_cache(self):
        try:
            luf = getLDAPPlugin()._getLDAPUserFolder()
        except KeyError:
            return []
        users = luf.getUsers(authenticated=1)
        for user in users:
            user.cache_type = 'authenticated'
        return users

    def nextURL(self):
        url = str(
            getMultiAdapter(
                (self.context, self.request), name=u"absolute_url"
            )
        )
        return url + "/@@ldap-controlpanel#" + self.request.form.get('fieldset_id', '')

    @property
    @memoize
    def storage(self):
        return getUtility(ILDAPConfiguration)

    def servers(self):
        def contype(c):
            if c==0:
                return "LDAP"
            elif c==1:
                return "LDAP over SSL"
            else:
                return "LDAP over IPC"

        return [dict(id=s.__name__,
                     enabled=s.enabled,
                     server=s.server,
                     connection_type=contype(s.connection_type),
                     connection_timeout=s.connection_timeout,
                     operation_timeout=s.operation_timeout)
                for s in self.storage.servers.values()]

    def schema(self):
        storage=self.storage

        def protected(attr):
            return attr.__name__ in storage.required_attributes + [
                    storage.rdn_attribute,
                    storage.userid_attribute,
                    storage.login_attribute]

        return [dict(id=p.__name__,
                     description=p.description,
                     ldap_name=p.ldap_name,
                     plone_name=p.plone_name,
                     multi_valued=p.multi_valued,
                     binary=p.binary,
                     protected=protected(p))
                for p in storage.schema.values()]

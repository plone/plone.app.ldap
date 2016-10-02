# -*- coding: utf-8 -*-
from Acquisition import Implicit
from Acquisition import aq_inner, aq_parent
from zope.component import getMultiAdapter
from zope.formlib.form import action, applyChanges
from zope.event import notify
from zope.i18nmessageid import MessageFactory
from zope.lifecycleevent import ObjectModifiedEvent
from Products.Five import BrowserView
try:  # >= 4.1
    from five.formlib.formbase import AddFormBase
    from five.formlib.formbase import EditFormBase
    AddFormBase, EditFormBase  # pyflakes
except ImportError:  # < 4.1
    from Products.Five.formlib.formbase import AddFormBase
    from Products.Five.formlib.formbase import EditFormBase
from plone.app.form.validators import null_validator

PMF = MessageFactory('plone')


class Adding(Implicit, BrowserView):
    __allow_access_to_unprotected_subobjects__ = True

    contentName = None
    request = None
    context = None

    def nextURL(self):
        return None

    def hasCustomAddView(self):
        return False

    def addingInfo(self):
        return []

    def isSingleMenuItem(self):
        return False


class LDAPAddForm(AddFormBase):
    """Base class for add forms.

    This class has a nextURL method which will return the URL of the LDAP
    management screen and standard form actions.
    """
    fieldset = None

    def nextURL(self):
        parent = aq_parent(aq_inner(self.context))
        url = str(getMultiAdapter((parent, self.request), name=u"absolute_url"))
        if self.fieldset is not None:
            return url + "/@@ldap-controlpanel#fieldsetlegend-" + self.fieldset

        return url + "/@@ldap-controlpanel"

    @action(PMF(u"label_save", default=u"Save"), name=u'save')
    def handle_save_action(self, action, data):
        self.createAndAdd(data)

    @action(PMF(u"label_cancel", default=u"Cancel"),
            validator=null_validator, name=u'cancel')
    def handle_cancel_action(self, action, data):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''


class LDAPEditForm(EditFormBase):
    """Base class for edit forms.

    This class has a nextURL method which will return the URL of the LDAP
    management screen and standard form actions.
    """
    fieldset = None

    @action(PMF(u"label_save", default=u"Save"), name=u'save')
    def handle_save_action(self, action, data):
        if applyChanges(self.context, self.form_fields, data, self.adapters):
            notify(ObjectModifiedEvent(self.context))
            self.status = "Changes saved"
        else:
            self.status = "No changes"

        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    @action(PMF(u"label_cancel", default=u"Cancel"),
            validator=null_validator, name=u'cancel')
    def handle_cancel_action(self, action, data):
        nextURL = self.nextURL()
        if nextURL:
            self.request.response.redirect(self.nextURL())
        return ''

    def nextURL(self):
        parent = aq_parent(aq_inner(self.context))
        url = str(getMultiAdapter((parent, self.request), name=u"absolute_url"))
        if self.fieldset is not None:
            return url + "/@@ldap-controlpanel#fieldsetlegend-" + self.fieldset

        return url + "/@@ldap-controlpanel"

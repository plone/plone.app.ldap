# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import logout
from plone.app.ldap.config import PROJECTNAME
from plone.app.ldap.testing import INTEGRATION_TESTING

import pkg_resources
import unittest

qi_dist = pkg_resources.get_distribution("Products.CMFQuickInstallerTool")
if qi_dist.parsed_version > pkg_resources.parse_version("3.0.9"):
    # This version uses the uninstall profile.
    SKIP_UNINSTALL_TEST = False
else:
    SKIP_UNINSTALL_TEST = True


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        view = api.content.get_view(
            u'ldap-controlpanel', self.portal, self.request)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@ldap-controlpanel')

    def test_controlpanel_installed(self):
        actions = [
            a.getAction(self)['id'] for a in self.controlpanel.listActions()]
        self.assertIn('ldap', actions)

    @unittest.skipIf(SKIP_UNINSTALL_TEST,
                     "uninstall not supported with this old quick installer")
    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        actions = [
            a.getAction(self)['id'] for a in self.controlpanel.listActions()]
        self.assertNotIn('ldap', actions)

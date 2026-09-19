from django.core.checks import Warning, registry
from django.test import SimpleTestCase

from bootstrap3.apps import check_bootstrap3_settings


class CheckBootstrap3SettingsTestCase(SimpleTestCase):
    def test_registered(self):
        """The check runs as part of manage.py check."""
        self.assertIn(check_bootstrap3_settings, registry.registry.get_checks())

    def test_known_settings_are_silent(self):
        with self.settings(BOOTSTRAP3={"include_jquery": True, "horizontal_label_class": "col-md-4"}):
            self.assertEqual(check_bootstrap3_settings(None), [])

    def test_empty_settings_are_silent(self):
        with self.settings(BOOTSTRAP3={}):
            self.assertEqual(check_bootstrap3_settings(None), [])

    def test_every_default_is_accepted(self):
        """No default key warns about itself."""
        from bootstrap3.bootstrap import BOOTSTRAP3_DEFAULTS

        with self.settings(BOOTSTRAP3=dict(BOOTSTRAP3_DEFAULTS)):
            self.assertEqual(check_bootstrap3_settings(None), [])

    def test_unknown_key_warns(self):
        with self.settings(BOOTSTRAP3={"no_such_setting": "value"}):
            warnings = check_bootstrap3_settings(None)
        self.assertEqual(len(warnings), 1)
        self.assertIsInstance(warnings[0], Warning)
        self.assertEqual(warnings[0].id, "bootstrap3.W001")
        self.assertEqual(
            warnings[0].msg,
            "BOOTSTRAP3['no_such_setting'] has no effect: not a django-bootstrap3 setting; it is ignored.",
        )

    def test_removed_setting_warns_with_its_own_hint(self):
        with self.settings(BOOTSTRAP3={"base_url": "/static/bootstrap/"}):
            warnings = check_bootstrap3_settings(None)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(
            warnings[0].msg,
            "BOOTSTRAP3['base_url'] has no effect: removed in 11.0.0, use `css_url` and `javascript_url`.",
        )

    def test_set_required_and_set_disabled_warn(self):
        with self.settings(BOOTSTRAP3={"set_required": True, "set_disabled": True}):
            warnings = check_bootstrap3_settings(None)
        self.assertEqual(len(warnings), 2)
        for warning in warnings:
            self.assertIn("removed in 11.0.0", warning.msg)

    def test_one_warning_per_unknown_key(self):
        with self.settings(BOOTSTRAP3={"theme_url": "/theme.css", "base_url": "/static/", "nope": 1}):
            warnings = check_bootstrap3_settings(None)
        self.assertEqual(len(warnings), 2)
        self.assertIn("base_url", warnings[0].msg)
        self.assertIn("nope", warnings[1].msg)

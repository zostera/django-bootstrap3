from django.test import TestCase, override_settings

from bootstrap3.bootstrap import get_bootstrap_setting
from tests.app.forms import TestForm, render_template_with_form


class SettingsTest(TestCase):
    def test_settings(self):
        from bootstrap3.bootstrap import get_bootstrap_setting

        self.assertTrue(get_bootstrap_setting("set_placeholder"))

    def test_bootstrap_javascript_tag(self):
        res = render_template_with_form("{% bootstrap_javascript %}")
        javascript_url = get_bootstrap_setting("javascript_url")
        self.assertHTMLEqual(
            res,
            '<script src="{url}" crossorigin="{crossorigin}" integrity="{integrity}"></script>'.format(
                **javascript_url
            ),
        )

    def test_bootstrap_css_tag(self):
        res = render_template_with_form("{% bootstrap_css %}").strip()
        css_url = get_bootstrap_setting("css_url")
        expected_html = (
            '<link href="{url}" crossorigin="{crossorigin}" integrity="{integrity}" rel="stylesheet">'.format(**css_url)
            + '<link href="//example.com/theme.css" rel="stylesheet">'
        )
        self.assertHTMLEqual(expected_html, res)

    def test_settings_filter(self):
        res = render_template_with_form('{{ "required_css_class"|bootstrap_setting }}')
        self.assertEqual(res.strip(), "bootstrap3-req")
        res = render_template_with_form('{% if "javascript_in_head"|bootstrap_setting %}head{% else %}body{% endif %}')
        self.assertEqual(res.strip(), "head")

    def test_required_class(self):
        form = TestForm()
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap3-req", res)

    def test_error_class(self):
        form = TestForm({})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap3-err", res)

    def test_bound_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap3-bound", res)

    @override_settings(BOOTSTRAP3={"css_url": None})
    def test_setting_to_none(self):
        css_url = get_bootstrap_setting("css_url")
        self.assertIsNone(css_url)

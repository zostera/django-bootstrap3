from django.contrib.messages import constants as message_constants
from django.forms import formset_factory
from django.template import Context, Template
from django.test import TestCase

from bootstrap3.components import render_alert
from bootstrap3.templatetags.bootstrap3 import bootstrap_message_classes
from tests.app.forms import TestForm


def render(template, context=None):
    return Template("{% load bootstrap3 %}" + template).render(Context(context or {}))


class RenderAlertTest(TestCase):
    """Alerts default to info and are dismissable unless asked otherwise."""

    def test_the_default_type_is_info(self):
        self.assertIn("alert-info", render_alert("Careful"))

    def test_an_explicit_type(self):
        self.assertIn("alert-danger", render_alert("Careful", alert_type="danger"))

    def test_dismissable_by_default(self):
        html = render_alert("Careful")
        self.assertIn("alert-dismissable", html)
        self.assertIn("data-dismiss", html)

    def test_not_dismissable(self):
        html = render_alert("Careful", dismissable=False)
        self.assertNotIn("alert-dismissable", html)
        self.assertNotIn("data-dismiss", html)


class MessageClassesTest(TestCase):
    """`bootstrap_message_classes` tolerates objects that are not Django messages."""

    class PlainMessage:
        def __init__(self, level=None, extra_tags=None):
            if level is not None:
                self.level = level
            if extra_tags is not None:
                self.extra_tags = extra_tags

    def test_a_message_with_a_level(self):
        self.assertIn("alert-danger", bootstrap_message_classes(self.PlainMessage(level=message_constants.ERROR)))

    def test_an_object_without_extra_tags(self):
        """Anything without the attribute is treated as having none."""
        self.assertIsInstance(bootstrap_message_classes(self.PlainMessage(level=message_constants.INFO)), str)

    def test_extra_tags_are_kept(self):
        classes = bootstrap_message_classes(self.PlainMessage(level=message_constants.INFO, extra_tags="mine"))
        self.assertIn("mine", classes)

    def test_an_object_without_a_level(self):
        self.assertIsInstance(bootstrap_message_classes(self.PlainMessage(extra_tags="mine")), str)


class CssAndJavascriptTagTest(TestCase):
    """The asset tags react to the configured URLs."""

    def test_css_without_a_theme(self):
        with self.settings(BOOTSTRAP3={"theme_url": None}):
            html = render("{% bootstrap_css %}")
        self.assertEqual(html.count("<link"), 1)

    def test_css_with_a_theme(self):
        with self.settings(BOOTSTRAP3={"theme_url": "//example.com/theme.css"}):
            html = render("{% bootstrap_css %}")
        self.assertIn("theme.css", html)

    def test_javascript_without_jquery(self):
        html = render("{% bootstrap_javascript %}")
        self.assertNotIn("jquery", html.lower())

    def test_javascript_with_jquery(self):
        html = render("{% bootstrap_javascript jquery=1 %}")
        self.assertIn("jquery", html.lower())

    def test_javascript_with_no_jquery_url_configured(self):
        with self.settings(BOOTSTRAP3={"jquery_url": None}):
            self.assertNotIn("jquery", render("{% bootstrap_javascript jquery=1 %}").lower())

    def test_javascript_with_no_javascript_url_configured(self):
        with self.settings(BOOTSTRAP3={"javascript_url": None}):
            self.assertEqual(render("{% bootstrap_javascript %}").strip(), "")


class ErrorTagTest(TestCase):
    """The standalone error tags."""

    def test_form_errors_tag(self):
        form = TestForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIsInstance(render("{% bootstrap_form_errors form %}", {"form": form}), str)

    def test_formset_errors_tag(self):
        formset_class = formset_factory(TestForm, extra=1)
        formset = formset_class(data={"form-TOTAL_FORMS": "1", "form-INITIAL_FORMS": "0"})
        self.assertIsInstance(render("{% bootstrap_formset_errors formset %}", {"formset": formset}), str)


class MessagesTagTest(TestCase):
    """`bootstrap_messages` accepts a plain dict as well as a Context."""

    def test_with_a_plain_dict(self):
        from bootstrap3.templatetags.bootstrap3 import bootstrap_messages

        html = bootstrap_messages({"messages": []})
        self.assertIsInstance(html, str)

    def test_through_a_template(self):
        html = render("{% bootstrap_messages %}")
        self.assertIsInstance(html, str)

from django import forms
from django.template import Context, Template, TemplateSyntaxError, Variable
from django.test import TestCase

from bootstrap3.utils import handle_var, remove_css_class, render_link_tag


class HandleVarTest(TestCase):
    """`handle_var` resolves a template value to a Python one."""

    def test_a_quoted_string_is_unquoted(self):
        self.assertEqual(handle_var('"hello"', Context({})), "hello")
        self.assertEqual(handle_var("'hello'", Context({})), "hello")

    def test_a_variable_is_resolved_from_the_context(self):
        self.assertEqual(handle_var("name", Context({"name": "value"})), "value")

    def test_an_unresolvable_variable_falls_back_to_the_string(self):
        self.assertEqual(handle_var("missing", Context({})), "missing")

    def test_a_template_variable_object_is_resolved(self):
        self.assertEqual(handle_var(Variable("name"), Context({"name": "value"})), "value")


class ParseTokenContentsTest(TestCase):
    """`parse_token_contents` splits a tag's arguments, via the tags that use it."""

    def render(self, template, context=None):
        return Template("{% load bootstrap3 %}" + template).render(Context(context or {}))

    def test_positional_and_keyword_arguments(self):
        html = self.render('{% bootstrap_button "Save" button_type="submit" %}')
        self.assertIn("Save", html)
        self.assertIn('type="submit"', html)

    def test_as_binds_the_result_to_a_variable(self):
        html = self.render('{% bootstrap_button "Save" as btn %}[{{ btn }}]')
        self.assertIn("[<button", html)

    def test_a_malformed_argument_is_rejected(self):
        """Django's own tokenizer never produces an empty bit, so this guards direct callers."""
        from bootstrap3.utils import parse_token_contents

        class FakeToken:
            def split_contents(self):
                return ["bootstrap_button", ""]

        with self.assertRaises(TemplateSyntaxError) as caught:
            parse_token_contents(parser=None, token=FakeToken())
        self.assertIn("Malformed arguments", str(caught.exception))


class RemoveCssClassTest(TestCase):
    def test_removes_only_the_named_classes(self):
        self.assertEqual(remove_css_class("a b c", "b"), "a c")

    def test_removes_several_at_once(self):
        self.assertEqual(remove_css_class("a b c", "a c"), "b")

    def test_a_class_that_is_not_there_changes_nothing(self):
        self.assertEqual(remove_css_class("a b", "z"), "a b")


class RenderLinkTagTest(TestCase):
    def test_without_media(self):
        self.assertHTMLEqual(
            render_link_tag("/style.css"),
            '<link href="/style.css" rel="stylesheet">',
        )

    def test_with_media(self):
        self.assertHTMLEqual(
            render_link_tag("/style.css", media="print"),
            '<link href="/style.css" media="print" rel="stylesheet">',
        )


class IsWidgetRequiredAttributeTest(TestCase):
    """`is_widget_required_attribute` decides whether to emit the required attribute."""

    def test_a_widget_that_is_not_required(self):
        from bootstrap3.forms import is_widget_required_attribute

        widget = forms.TextInput()
        widget.is_required = False
        self.assertFalse(is_widget_required_attribute(widget))

    def test_a_required_text_input(self):
        from bootstrap3.forms import is_widget_required_attribute

        widget = forms.TextInput()
        widget.is_required = True
        self.assertTrue(is_widget_required_attribute(widget))

    def test_a_widget_type_that_never_carries_required(self):
        from bootstrap3.forms import WIDGETS_NO_REQUIRED, is_widget_required_attribute

        widget = WIDGETS_NO_REQUIRED[0]()
        widget.is_required = True
        self.assertFalse(is_widget_required_attribute(widget))


class ButtonsTagTest(TestCase):
    """`{% buttons %}` is the tag that parses its own arguments."""

    def render(self, template, context=None):
        return Template("{% load bootstrap3 %}" + template).render(Context(context or {}))

    def test_submit_and_reset_buttons(self):
        html = self.render('{% buttons submit="OK" reset="Cancel" %}{% endbuttons %}')
        self.assertIn('type="submit"', html)
        self.assertIn("OK", html)
        self.assertIn('type="reset"', html)
        self.assertIn("Cancel", html)

    def test_content_between_the_tags_is_kept(self):
        html = self.render("{% buttons %}<span>extra</span>{% endbuttons %}")
        self.assertIn("<span>extra</span>", html)

    def test_a_keyword_value_is_resolved_from_the_context(self):
        html = self.render("{% buttons submit=label %}{% endbuttons %}", {"label": "Send"})
        self.assertIn("Send", html)

    def test_as_binds_the_output_and_renders_nothing_in_place(self):
        """
        The tag itself emits nothing; the bound value carries the markup.

        The bound value is a plain `str` rather than marked safe, so rendering it with
        `{{ block }}` escapes it. Pinning current behaviour: `{{ block|safe }}` is what a
        caller needs today.
        """
        html = self.render("{% buttons submit='OK' as block %}{% endbuttons %}[{{ block }}]")
        self.assertTrue(html.strip().startswith("["), html.strip()[:40])
        self.assertIn("type=&quot;submit&quot;", html)

        safe = self.render("{% buttons submit='OK' as block %}{% endbuttons %}{{ block|safe }}")
        self.assertIn('type="submit"', safe)

    def test_a_positional_argument_is_accepted(self):
        """The tag takes positional arguments even though it uses none of them."""
        self.render('{% buttons "ignored" submit="OK" %}{% endbuttons %}')

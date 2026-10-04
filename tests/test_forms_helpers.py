from django.forms import formset_factory
from django.test import TestCase

from bootstrap3.exceptions import BootstrapError
from bootstrap3.forms import render_button, render_form_errors, render_formset_errors
from tests.app.forms import TestForm


class RenderButtonSizeTest(TestCase):
    """`size` maps to a Bootstrap button size class."""

    def test_sizes(self):
        for size, expected in (
            ("xs", "btn-xs"),
            ("sm", "btn-sm"),
            ("small", "btn-sm"),
            ("lg", "btn-lg"),
            ("large", "btn-lg"),
        ):
            with self.subTest(size=size):
                self.assertIn(expected, render_button("Click", size=size))

    def test_medium_adds_no_size_class(self):
        for size in ("md", "medium"):
            with self.subTest(size=size):
                html = render_button("Click", size=size)
                self.assertNotIn("btn-xs", html)
                self.assertNotIn("btn-sm", html)
                self.assertNotIn("btn-lg", html)

    def test_an_empty_size_adds_no_size_class(self):
        self.assertNotIn("btn-", render_button("Click", size="").replace("btn-default", ""))

    def test_an_unknown_size_is_rejected(self):
        with self.assertRaises(BootstrapError) as caught:
            render_button("Click", size="enormous")
        self.assertIn('should be "xs", "sm", "lg" or empty', str(caught.exception))


class RenderButtonTypeTest(TestCase):
    def test_each_allowed_type(self):
        for button_type in ("submit", "reset", "button"):
            with self.subTest(button_type=button_type):
                self.assertIn(f'type="{button_type}"', render_button("Click", button_type=button_type))

    def test_link_renders_an_anchor_without_a_type(self):
        html = render_button("Click", button_type="link", href="/go")
        self.assertIn("<a", html)
        self.assertIn('href="/go"', html)

    def test_an_unknown_type_is_rejected(self):
        with self.assertRaises(BootstrapError) as caught:
            render_button("Click", button_type="explode")
        self.assertIn('should be "submit", "reset", "button", "link" or empty', str(caught.exception))


class RenderButtonAttributesTest(TestCase):
    """The optional attributes are only emitted when given."""

    def test_each_attribute_is_emitted(self):
        html = render_button("Click", id="go", name="action", value="save", title="Save it")
        self.assertIn('id="go"', html)
        self.assertIn('name="action"', html)
        self.assertIn('value="save"', html)
        self.assertIn('title="Save it"', html)

    def test_none_are_emitted_by_default(self):
        html = render_button("Click")
        for attribute in ("id=", "name=", "value=", "title="):
            self.assertNotIn(attribute, html)

    def test_an_href_makes_it_an_anchor(self):
        self.assertIn("<a", render_button("Click", href="/go"))

    def test_without_an_href_it_is_a_button(self):
        self.assertIn("<button", render_button("Click"))


class RenderErrorsTest(TestCase):
    """The standalone error renderers."""

    def test_form_errors(self):
        form = TestForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIsInstance(render_form_errors(form), str)

    def test_form_errors_for_all_error_types(self):
        form = TestForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required", render_form_errors(form, error_types="all"))

    def test_formset_errors(self):
        formset_class = formset_factory(TestForm, extra=1)
        formset = formset_class(data={"form-TOTAL_FORMS": "1", "form-INITIAL_FORMS": "0"})
        self.assertIsInstance(render_formset_errors(formset), str)


class RenderFieldAndLabelTest(TestCase):
    """Horizontal layout fills in the classes the caller did not supply."""

    def test_horizontal_defaults_are_used_when_nothing_is_given(self):
        from bootstrap3.forms import render_field_and_label

        html = render_field_and_label("<input>", "Label", layout="horizontal")
        self.assertIn("control-label", html)
        self.assertIn("col-md-", html)

    def test_explicit_classes_and_label_are_left_alone(self):
        from bootstrap3.forms import render_field_and_label

        html = render_field_and_label(
            "<input>", "Label", layout="horizontal", label_class="my-label", field_class="my-field"
        )
        self.assertIn("my-label", html)
        self.assertIn("my-field", html)
        self.assertIn("control-label", html)

    def test_an_empty_label_becomes_a_non_breaking_space(self):
        from bootstrap3.forms import render_field_and_label

        html = render_field_and_label("<input>", "", layout="horizontal")
        self.assertIn("&#160;", html)

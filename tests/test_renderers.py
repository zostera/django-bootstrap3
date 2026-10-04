from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
from django.forms import formset_factory
from django.test import TestCase

from bootstrap3.exceptions import BootstrapError
from bootstrap3.renderers import BaseRenderer, FieldRenderer, FormRenderer, FormsetRenderer
from tests.app.forms import TestForm, render_form_field


class SelectDateForm(forms.Form):
    when = forms.DateField(widget=forms.SelectDateWidget)


class FileForm(forms.Form):
    attachment = forms.FileField(widget=forms.ClearableFileInput, required=False)


class PasswordHashForm(forms.Form):
    password = forms.CharField(widget=ReadOnlyPasswordHashWidget, required=False)


class ComplainingFormSet(forms.BaseFormSet):
    def clean(self):
        raise forms.ValidationError("Formset-level problem.")


class BaseRendererTest(TestCase):
    def test_render_of_the_base_class_is_empty(self):
        """BaseRenderer._render is a no-op that subclasses override."""
        renderer = BaseRenderer()
        self.assertEqual(renderer._render(), "")

    def test_an_invalid_size_is_rejected(self):
        with self.assertRaises(BootstrapError) as caught:
            BaseRenderer(size="enormous")
        self.assertIn('Invalid value "enormous"', str(caught.exception))

    def test_the_accepted_sizes(self):
        for size, expected in (
            ("sm", "small"),
            ("small", "small"),
            ("lg", "large"),
            ("large", "large"),
            ("md", "medium"),
            ("medium", "medium"),
            ("", "medium"),
        ):
            with self.subTest(size=size):
                self.assertEqual(BaseRenderer(size=size).size, expected)


class FormErrorTypesTest(TestCase):
    def test_an_illegal_error_type_is_rejected(self):
        form = TestForm(data={})
        form.is_valid()
        with self.assertRaises(Exception) as caught:
            FormRenderer(form).render_errors(error_types="nonsense")
        self.assertIn("Illegal value", str(caught.exception))

    def test_none_renders_nothing(self):
        form = TestForm(data={})
        form.is_valid()
        self.assertEqual(FormRenderer(form).render_errors(error_types="none"), "")


class FormsetErrorsTest(TestCase):
    def test_non_form_errors_are_rendered(self):
        formset_class = formset_factory(TestForm, formset=ComplainingFormSet, extra=1)
        formset = formset_class(data={"form-TOTAL_FORMS": "1", "form-INITIAL_FORMS": "0"})
        self.assertFalse(formset.is_valid())
        self.assertIn("Formset-level problem.", FormsetRenderer(formset).render_errors())


class WidgetSpecificMarkupTest(TestCase):
    """Widgets that need their rendered HTML rearranged."""

    def test_select_date_widget_is_wrapped_in_a_row(self):
        html = render_form_field("when", context={"form": SelectDateForm()})
        self.assertIn("bootstrap3-multi-input", html)
        self.assertIn("col-xs-4", html)

    def test_clearable_file_input_is_wrapped_in_a_row(self):
        html = render_form_field("attachment", context={"form": FileForm()})
        self.assertIn("bootstrap3-multi-input", html)
        self.assertIn("col-xs-12", html)

    def test_read_only_password_hash_widget_is_a_static_control(self):
        html = render_form_field("password", context={"form": PasswordHashForm()})
        self.assertIn("form-control-static", html)


class RendererHelperDefaultsTest(TestCase):
    """The widget argument of these helpers defaults to the renderer's own widget."""

    def _renderer(self):
        return FieldRenderer(TestForm()["subject"])

    def test_add_class_attrs_defaults_to_own_widget(self):
        renderer = self._renderer()
        renderer.widget.attrs.pop("class", None)
        renderer.add_class_attrs()
        self.assertIn("form-control", renderer.widget.attrs["class"])

    def test_add_placeholder_attrs_defaults_to_own_widget(self):
        renderer = self._renderer()
        renderer.widget.attrs.pop("placeholder", None)
        renderer.add_placeholder_attrs()
        self.assertIn("placeholder", renderer.widget.attrs)

    def test_add_help_attrs_defaults_to_own_widget(self):
        renderer = self._renderer()
        renderer.widget.attrs.pop("title", None)
        renderer.add_help_attrs()
        self.assertIn("title", renderer.widget.attrs)


class PlaceholderTest(TestCase):
    """Where the placeholder comes from."""

    def test_it_defaults_to_the_label(self):
        renderer = FieldRenderer(TestForm()["subject"])
        self.assertEqual(renderer.placeholder, TestForm()["subject"].label)

    def test_an_explicit_empty_placeholder_is_honoured(self):
        renderer = FieldRenderer(TestForm()["subject"], placeholder="")
        self.assertEqual(renderer.placeholder, "")

    def test_set_placeholder_off_leaves_it_empty(self):
        with self.settings(BOOTSTRAP3={"set_placeholder": False}):
            renderer = FieldRenderer(TestForm()["subject"])
        self.assertEqual(renderer.placeholder, "")

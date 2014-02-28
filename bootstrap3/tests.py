from __future__ import unicode_literals


from django import forms
from django.template import Template, Context
from django.utils.unittest import TestCase

from .exceptions import BootstrapError


RADIO_CHOICES = (
    ('1', 'Radio 1'),
    ('2', 'Radio 2'),
)

MEDIA_CHOICES = (
    ('Audio', (
        ('vinyl', 'Vinyl'),
        ('cd', 'CD'),
    )
    ),
    ('Video', (
        ('vhs', 'VHS Tape'),
        ('dvd', 'DVD'),
    )
    ),
    ('unknown', 'Unknown'),
)


class TestForm(forms.Form):
    """
    Form with a variety of widgets to test bootstrap3 rendering.
    """
    subject = forms.CharField(
        max_length=100,
        help_text='my_help_text',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'placeholdertest'}),
    )
    message = forms.CharField(required=False, help_text='<i>my_help_text</i>')
    sender = forms.EmailField()
    secret = forms.CharField(initial=42, widget=forms.HiddenInput)
    cc_myself = forms.BooleanField(required=False, help_text='You will get a copy in your mailbox.')
    select1 = forms.ChoiceField(choices=RADIO_CHOICES)
    select2 = forms.MultipleChoiceField(
        choices=RADIO_CHOICES,
        help_text='Check as many as you like.',
    )
    select3 = forms.ChoiceField(choices=MEDIA_CHOICES)
    select4 = forms.MultipleChoiceField(
        choices=MEDIA_CHOICES,
        help_text='Check as many as you like.',
    )
    category1 = forms.ChoiceField(choices=RADIO_CHOICES, widget=forms.RadioSelect)
    category2 = forms.MultipleChoiceField(
        choices=RADIO_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text='Check as many as you like.',
    )
    category3 = forms.ChoiceField(widget=forms.RadioSelect, choices=MEDIA_CHOICES)
    category4 = forms.MultipleChoiceField(
        choices=MEDIA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text='Check as many as you like.',
    )

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data


def render_template(text, **context_args):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    template = Template("{% load bootstrap3 %}" + text)
    if not 'form' in context_args:
        context_args['form'] = TestForm()
    return template.render(Context(context_args))


def render_formset(formset=None, **context_args):
    """
    Create a template that renders a formset
    """
    context_args['formset'] = formset
    return render_template('{% bootstrap_formset formset %}', **context_args)


def render_form(form=None, **context_args):
    """
    Create a template that renders a form
    """
    if form:
        context_args['form'] = form
    return render_template('{% bootstrap_form form %}', **context_args)


def render_form_field(field, **context_args):
    """
    Create a template that renders a field
    """
    form_field = 'form.%s' % field
    return render_template('{% bootstrap_field ' + form_field + ' %}', **context_args)


def render_field(field, **context_args):
    """
    Create a template that renders a field
    """
    context_args['field'] = field
    return render_template('{% bootstrap_field field %}', **context_args)


class SettingsTest(TestCase):

    def test_settings(self):
        from .bootstrap import BOOTSTRAP3
        self.assertTrue(BOOTSTRAP3)


class TemplateTest(TestCase):

    def test_empty_template(self):
        res = render_template('')
        self.assertEqual(res.strip(), '')

    def test_text_template(self):
        res = render_template('some text')
        self.assertEqual(res.strip(), 'some text')

    def test_bootstrap_template(self):
        template = Template(('{% extends "bootstrap3/bootstrap3.html" %}{% block bootstrap3_content %}test_bootstrap3_content{% endblock %}'))
        res = template.render(Context({}))
        self.assertIn('test_bootstrap3_content', res)

    def test_javascript_without_jquery(self):
        res = render_template('{% bootstrap_javascript jquery=0 %}')
        self.assertIn('bootstrap', res)
        self.assertNotIn('jquery', res)

    def test_javascript_with_jquery(self):
        res = render_template('{% bootstrap_javascript jquery=1 %}')
        self.assertIn('bootstrap', res)
        self.assertIn('jquery', res)


class FormSetTest(TestCase):

    def test_illegal_formset(self):
        with self.assertRaises(BootstrapError):
            render_formset(formset='illegal')


class FormTest(TestCase):

    def test_illegal_form(self):
        with self.assertRaises(BootstrapError):
            render_form(form='illegal')

    def test_field_names(self):
        form = TestForm()
        res = render_form(form)
        for field in form:
            self.assertIn('name="%s"' % field.name, res)

    def test_exclude(self):
        form = TestForm()
        res = render_template('{% bootstrap_form form exclude="cc_myself" %}', form=form)
        self.assertNotIn('cc_myself', res)

    def test_layout_horizontal(self):
        form = TestForm()
        res = render_template('{% bootstrap_form form layout="horizontal" %}', form=form)
        self.assertIn('col-md-2', res)
        self.assertIn('col-md-4', res)

    def test_buttons_tag(self):
        form = TestForm()
        res = render_template('{% buttons layout="horizontal" %}{% endbuttons %}', form=form)
        self.assertIn('col-md-2', res)
        self.assertIn('col-md-4', res)


class FieldTest(TestCase):

    def test_illegal_field(self):
        with self.assertRaises(BootstrapError):
            render_field(field='illegal')

    def test_show_help(self):
        res = render_form_field('subject')
        self.assertIn('my_help_text', res)
        self.assertNotIn('<i>my_help_text</i>', res)
        res = render_template('{% bootstrap_field form.subject show_help=0 %}')
        self.assertNotIn('my_help_text', res)

    def test_subject(self):
        res = render_form_field('subject')
        self.assertIn('type="text"', res)
        self.assertIn('placeholder="placeholdertest"', res)

    def test_required_field(self):
        required_field = render_form_field('subject')
        self.assertIn('required', required_field)
        not_required_field = render_form_field('message')
        self.assertNotIn('required', not_required_field)
        # Required field with required=0
        form_field = 'form.subject'
        rendered = render_template('{% bootstrap_field ' + form_field + ' set_required=0 %}')
        self.assertNotIn('required', rendered)


class IconTest(TestCase):

    def test_icon(self):
        res = render_template('{% bootstrap_icon "star" %}')
        self.assertEqual(res.strip(), '<span class="glyphicon glyphicon-star"></span>')


class MessagesTest(TestCase):

    def test_messages(self):
        class FakeMessage(object):
            """
            Follows the `django.contrib.messages.storage.base.Message` API.
            """
            def __init__(self, message, tags):
                self.tags = tags
                self.message = message

            def __str__(self):
                return self.message

        messages = [FakeMessage("hello", "warning")]
        res = render_template('{% bootstrap_messages messages %}', messages=messages)
        expected = """
    <div class="alert alert-warning alert-dismissable">
        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
        hello
    </div>
"""
        self.assertEqual(res.strip(), expected.strip())

        messages = [FakeMessage("hello", "error")]
        res = render_template('{% bootstrap_messages messages %}', messages=messages)
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
        hello
    </div>
        """
        self.assertEqual(res.strip(), expected.strip())

        messages = [FakeMessage("hello", None)]
        res = render_template('{% bootstrap_messages messages %}', messages=messages)
        expected = """
    <div class="alert alert-dismissable">
        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>
        hello
    </div>
"""
        self.assertEqual(res.strip(), expected.strip())

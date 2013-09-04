from __future__ import unicode_literals

from django.template import Template, Context
from unittest import TestCase
from django import forms


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
    subject = forms.CharField(max_length=100, help_text='Maximum 100 chars.')
    message = forms.CharField()
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


def render_form(form=None, **context_args):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    if form:
        context_args['form'] = form
    return render_template('{% bootstrap_form form %}', **context_args)


def render_field(field, **context_args):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    form_field = 'form.%s' % field
    return render_template('{% bootstrap_field ' + form_field + ' %}', **context_args)


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


class FormTest(TestCase):

    def test_field_names(self):
        form = TestForm()
        res = render_form(form)
        for field in form:
            self.assertIn('name="%s"' % field.name, res)


class FieldTest(TestCase):

    def test_subject(self):
        res = render_field('subject')
        self.assertIn('type="text"', res)


class IconTest(TestCase):

    def test_subject(self):
        res = render_template('{% bootstrap_icon "star" %}')
        self.assertEqual(res.strip(), '<span class="glyphicon glyphicon-star"></span>')

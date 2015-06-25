# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.test import TestCase

from django import forms
from django.forms.formsets import formset_factory
from django.template import Template, Context

from .text import text_value, text_concat
from .exceptions import BootstrapError
from .utils import add_css_class

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser


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
    date = forms.DateField(required=False)
    subject = forms.CharField(
        max_length=100,
        help_text='my_help_text',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'placeholdertest'}),
    )
    password = forms.CharField(widget=forms.PasswordInput)
    message = forms.CharField(required=False, help_text='<i>my_help_text</i>')
    sender = forms.EmailField(
        label='Sender © unicode',
        help_text='E.g., "me@example.com"')
    secret = forms.CharField(initial=42, widget=forms.HiddenInput)
    cc_myself = forms.BooleanField(
        required=False,
        help_text='cc stands for "carbon copy." '
                  'You will get a copy in your mailbox.'
    )
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
    category1 = forms.ChoiceField(
        choices=RADIO_CHOICES, widget=forms.RadioSelect)
    category2 = forms.MultipleChoiceField(
        choices=RADIO_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text='Check as many as you like.',
    )
    category3 = forms.ChoiceField(
        widget=forms.RadioSelect, choices=MEDIA_CHOICES)
    category4 = forms.MultipleChoiceField(
        choices=MEDIA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text='Check as many as you like.',
    )
    addon = forms.CharField(
        widget=forms.TextInput(attrs={'addon_before': 'before', 'addon_after': 'after'}),
    )

    required_css_class = 'bootstrap3-req'

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        raise forms.ValidationError(
            "This error was added to show the non field errors styling.")
        return cleaned_data


class TestFormWithoutRequiredClass(TestForm):
    required_css_class = ''


def render_template(text, **context_args):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    template = Template("{% load bootstrap3 %}" + text)
    if 'form' not in context_args:
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
    return render_template(
        '{% bootstrap_field ' + form_field + ' %}', **context_args)


def render_field(field, **context_args):
    """
    Create a template that renders a field
    """
    context_args['field'] = field
    return render_template('{% bootstrap_field field %}', **context_args)


def get_title_from_html(html):
    class GetTitleParser(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.title = None

        def handle_starttag(self, tag, attrs):
            for attr, value in attrs:
                if attr == 'title':
                    self.title = value

    parser = GetTitleParser()
    parser.feed(html)

    return parser.title


class SettingsTest(TestCase):
    def test_settings(self):
        from .bootstrap import BOOTSTRAP3
        self.assertTrue(BOOTSTRAP3)

    def test_bootstrap_javascript_tag(self):
        res = render_template('{% bootstrap_javascript %}')
        self.assertEqual(res.strip(), '<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>')

    def test_bootstrap_css_tag(self):
        res = render_template('{% bootstrap_css %}')
        self.assertEqual(res.strip(), '<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css" rel="stylesheet">')

    def test_settings_filter(self):
        res = render_template('{{ "required_css_class"|bootstrap_setting }}')
        self.assertEqual(res.strip(), 'bootstrap3-req')
        res = render_template('{% if "javascript_in_head"|bootstrap_setting %}head{% else %}body{% endif %}')
        self.assertEqual(res.strip(), 'head')

    def test_required_class(self):
        form = TestForm()
        res = render_template('{% bootstrap_form form %}', form=form)
        self.assertIn('bootstrap3-req', res)

    def test_error_class(self):
        form = TestForm({})
        res = render_template('{% bootstrap_form form %}', form=form)
        self.assertIn('bootstrap3-err', res)

    def test_bound_class(self):
        form = TestForm({'sender': 'sender'})
        res = render_template('{% bootstrap_form form %}', form=form)
        self.assertIn('bootstrap3-bound', res)


class TemplateTest(TestCase):
    def test_empty_template(self):
        res = render_template('')
        self.assertEqual(res.strip(), '')

    def test_text_template(self):
        res = render_template('some text')
        self.assertEqual(res.strip(), 'some text')

    def test_bootstrap_template(self):
        template = Template((
            '{% extends "bootstrap3/bootstrap3.html" %}' +
            '{% block bootstrap3_content %}' +
            'test_bootstrap3_content' +
            '{% endblock %}'
        ))
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

    def test_field_addons(self):
        form = TestForm()
        res = render_form(form)
        self.assertIn('<div class="input-group"><span class="input-group-addon">before</span><input', res)
        self.assertIn('/><span class="input-group-addon">after</span></div>', res)

    def test_exclude(self):
        form = TestForm()
        res = render_template(
            '{% bootstrap_form form exclude="cc_myself" %}', form=form)
        self.assertNotIn('cc_myself', res)

    def test_layout_horizontal(self):
        form = TestForm()
        res = render_template(
            '{% bootstrap_form form layout="horizontal" %}', form=form)
        self.assertIn('col-md-3', res)
        self.assertIn('col-md-9', res)
        res = render_template(
            '{% bootstrap_form form layout="horizontal" ' +
            'horizontal_label_class="hlabel" ' +
            'horizontal_field_class="hfield" %}',
            form=form
        )
        self.assertIn('hlabel', res)
        self.assertIn('hfield', res)

    def test_buttons_tag(self):
        form = TestForm()
        res = render_template(
            '{% buttons layout="horizontal" %}{% endbuttons %}', form=form)
        self.assertIn('col-md-3', res)
        self.assertIn('col-md-9', res)


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

    def test_help_with_quotes(self):
        # Checkboxes get special handling, so test a checkbox and something else
        res = render_form_field('sender')
        self.assertEqual(get_title_from_html(res), TestForm.base_fields['sender'].help_text)

        res = render_form_field('cc_myself')
        self.assertEqual(get_title_from_html(res), TestForm.base_fields['cc_myself'].help_text)

    def test_subject(self):
        res = render_form_field('subject')
        self.assertIn('type="text"', res)
        self.assertIn('placeholder="placeholdertest"', res)

    def test_password(self):
        res = render_form_field('password')
        self.assertIn('type="password"', res)
        self.assertIn('placeholder="Password"', res)

    def test_required_field(self):
        required_field = render_form_field('subject')
        self.assertIn('required', required_field)
        self.assertIn('bootstrap3-req', required_field)
        not_required_field = render_form_field('message')
        self.assertNotIn('required', not_required_field)
        # Required field with required=0
        form_field = 'form.subject'
        rendered = render_template(
            '{% bootstrap_field ' + form_field + ' set_required=0 %}')
        self.assertNotIn('required', rendered)
        # Required settings in field
        form_field = 'form.subject'
        rendered = render_template(
            '{% bootstrap_field ' +
            form_field +
            ' required_css_class="test-required" %}')
        self.assertIn('test-required', rendered)

    def test_empty_permitted(self):
        form = TestForm()
        res = render_form_field('subject', form=form)
        self.assertIn('required', res)
        form.empty_permitted = True
        res = render_form_field('subject', form=form)
        self.assertNotIn('required', res)

    def test_input_group(self):
        res = render_template(
            '{% bootstrap_field form.subject addon_before="$" ' +
            'addon_after=".00" %}'
        )
        self.assertIn('class="input-group"', res)
        self.assertIn('class="input-group-addon">$', res)
        self.assertIn('class="input-group-addon">.00', res)

    def test_size(self):
        def _test_size(param, klass):
            res = render_template(
                '{% bootstrap_field form.subject size="' + param + '" %}')
            self.assertIn(klass, res)

        def _test_size_medium(param):
            res = render_template(
                '{% bootstrap_field form.subject size="' + param + '" %}')
            self.assertNotIn('input-lg', res)
            self.assertNotIn('input-sm', res)
            self.assertNotIn('input-md', res)
        _test_size('sm', 'input-sm')
        _test_size('small', 'input-sm')
        _test_size('lg', 'input-lg')
        _test_size('large', 'input-lg')
        _test_size_medium('md')
        _test_size_medium('medium')
        _test_size_medium('')


class ComponentsTest(TestCase):
    def test_icon(self):
        res = render_template('{% bootstrap_icon "star" %}')
        self.assertEqual(
            res.strip(), '<span class="glyphicon glyphicon-star"></span>')
        res = render_template(
            '{% bootstrap_icon "star" title="alpha centauri" %}')
        self.assertEqual(
            res.strip(),
            '<span class="glyphicon glyphicon-star" ' +
            'title="alpha centauri"></span>')

    def test_alert(self):
        res = render_template(
            '{% bootstrap_alert "content" alert_type="danger" %}')
        self.assertEqual(
            res.strip(),
            '<div class="alert alert-danger alert-dismissable">' +
            '<button type="button" class="close" data-dismiss="alert" ' +
            'aria-hidden="true">' +
            '&times;</button>content</div>'
        )


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

        pattern = re.compile(r'\s+')
        messages = [FakeMessage("hello", "warning")]
        res = render_template(
            '{% bootstrap_messages messages %}', messages=messages)
        expected = """
    <div class="alert alert-warning alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello
    </div>
"""
        self.assertEqual(
            re.sub(pattern, '', res),
            re.sub(pattern, '', expected)
        )

        messages = [FakeMessage("hello", "error")]
        res = render_template(
            '{% bootstrap_messages messages %}', messages=messages)
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello
    </div>
        """
        self.assertEqual(
            re.sub(pattern, '', res),
            re.sub(pattern, '', expected)
        )

        messages = [FakeMessage("hello", None)]
        res = render_template(
            '{% bootstrap_messages messages %}', messages=messages)
        expected = """
    <div class="alert alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello
    </div>
        """

        self.assertEqual(
            re.sub(pattern, '', res),
            re.sub(pattern, '', expected)
        )


class TextTest(TestCase):
    def test_add_css_class(self):
        css_classes = "one two"
        css_class = "three four"
        classes = add_css_class(css_classes, css_class)
        self.assertEqual(classes, "one two three four")

        classes = add_css_class(css_classes, css_class, prepend=True)
        self.assertEqual(classes, "three four one two")


class HtmlTest(TestCase):
    def test_text_value(self):
        self.assertEqual(text_value(''), "")
        self.assertEqual(text_value(' '), " ")
        self.assertEqual(text_value(None), "")
        self.assertEqual(text_value(1), "1")

    def test_text_concat(self):
        self.assertEqual(text_concat(1, 2), "12")
        self.assertEqual(text_concat(1, 2, separator='='), "1=2")
        self.assertEqual(text_concat(None, 2, separator='='), "2")


class ButtonTest(TestCase):
    def test_button(self):
        res = render_template(
            "{% bootstrap_button 'button' size='lg' %}")
        self.assertEqual(
            res.strip(), '<button class="btn btn-lg">button</button>')
        res = render_template(
            "{% bootstrap_button 'button' size='lg' href='#' %}")
        self.assertIn(
            res.strip(),
            '<a class="btn btn-lg" href="#">button</a><a href="#" ' +
            'class="btn btn-lg">button</a>')


class ShowLabelTest(TestCase):
    def test_show_label(self):
        form = TestForm()
        res = render_template(
            '{% bootstrap_form form show_label=False %}',
            form=form
        )
        self.assertIn('sr-only', res)

    def test_for_formset(self):
        TestFormSet = formset_factory(TestForm, extra=1)
        test_formset = TestFormSet()
        res = render_template(
            '{% bootstrap_formset formset show_label=False %}',
            formset=test_formset
        )
        self.assertIn('sr-only', res)

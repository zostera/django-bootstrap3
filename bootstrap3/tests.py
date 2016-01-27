# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.forms.forms import Form
from django.test import TestCase

from django import forms
from django.forms.formsets import formset_factory
from django.template import Template, Context
from django.contrib.admin.widgets import AdminSplitDateTime

from bootstrap3.exceptions import BootstrapException
from bootstrap3.layout import FieldContainer, LayoutFormRenderer, Col, Row, LayoutElement, Layout, \
    EllipsisFieldContainer
from .text import text_value, text_concat
from .exceptions import BootstrapError
from .utils import add_css_class, render_tag, render_template_to_unicode

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
    datetime = forms.SplitDateTimeField(widget=AdminSplitDateTime(), required=False)
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
        help_text='cc stands for "carbon copy." You will get a copy in your mailbox.'
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


class WellLayoutElement(LayoutElement):
    """
    fake LayoutElement that display a field in a well
    """


    def _render(self, form, renderer):
        """
        render the children into a div with well class
        """
        return render_tag(
            'div',
            attrs={
                "class": "well"
            },
            content=self._render_children(form, renderer)
        )

def render_template(text, **context_args):
    """
    Create a template ``text`` that first loads bootstrap3.
    """
    template = Template("{% load bootstrap3 %}" + text)
    if 'form' not in context_args:
        context_args['form'] = TestForm()
    return render_template_to_unicode(template, context=context_args)


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
        self.assertEqual(
            res.strip(),
            '<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>'
        )

    def test_bootstrap_css_tag(self):
        res = render_template('{% bootstrap_css %}')
        self.assertIn(res.strip(), [
            '<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">',
            '<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">',
        ])

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
        res = render_template_to_unicode(template)
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
            # datetime has a multiwidget field widget
            if field.name == "datetime":
                self.assertIn('name="datetime_0"', res)
                self.assertIn('name="datetime_1"', res)
            else:
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

    def test_error_class(self):
        form = TestForm({'sender': 'sender'})
        res = render_template('{% bootstrap_form form %}', form=form)
        self.assertIn('bootstrap3-err', res)

        res = render_template(
            '{% bootstrap_form form error_css_class="successful-test" %}',
            form=form
        )
        self.assertIn('successful-test', res)

        res = render_template('{% bootstrap_form form error_css_class="" %}',
                              form=form)
        self.assertNotIn('bootstrap3-err', res)

    def test_required_class(self):
        form = TestForm({'sender': 'sender'})
        res = render_template('{% bootstrap_form form %}', form=form)
        self.assertIn('bootstrap3-req', res)

        res = render_template(
            '{% bootstrap_form form required_css_class="successful-test" %}',
            form=form
        )
        self.assertIn('successful-test', res)

        res = render_template('{% bootstrap_form form required_css_class="" %}',
                              form=form)
        self.assertNotIn('bootstrap3-req', res)

    def test_bound_class(self):
        form = TestForm({'sender': 'sender'})
        res = render_template('{% bootstrap_form form %}', form=form)
        self.assertIn('bootstrap3-bound', res)

        res = render_template(
            '{% bootstrap_form form bound_css_class="successful-test" %}',
            form=form
        )
        self.assertIn('successful-test', res)

        res = render_template('{% bootstrap_form form bound_css_class="" %}',
                              form=form)
        self.assertNotIn('bootstrap3-bound', res)


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

    def test_datetime(self):
        field = render_form_field('datetime')
        self.assertIn('vDateField', field)
        self.assertIn('vTimeField', field)

    def test_field_same_render(self):
        form = TestForm()
        rendered_a = render_form_field("addon", form=form)
        rendered_b = render_form_field("addon", form=form)
        self.assertEqual(rendered_a, rendered_b)

    def test_attributes_consistency(self):
        form = TestForm()
        attrs = form.fields['addon'].widget.attrs.copy()
        field_alone = render_form_field("addon", form=form)
        self.assertEqual(attrs, form.fields['addon'].widget.attrs)

class ComponentsTest(TestCase):
    def test_icon(self):
        res = render_template('{% bootstrap_icon "star" %}')
        self.assertEqual(
            res.strip(), '<span class="glyphicon glyphicon-star"></span>')
        res = render_template(
            '{% bootstrap_icon "star" title="alpha centauri" %}')
        self.assertIn(res.strip(), [
            '<span class="glyphicon glyphicon-star" title="alpha centauri"></span>',
            '<span title="alpha centauri" class="glyphicon glyphicon-star"></span>',
        ])

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

        messages = [FakeMessage("hello http://example.com", "error")]
        res = render_template(
            '{% bootstrap_messages messages %}', messages=messages)
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello <a href="http://example.com">http://example.com</a>
    </div>
        """
        self.assertEqual(
            re.sub(pattern, '', res).replace('rel="nofollow"', ''),
            re.sub(pattern, '', expected).replace('rel="nofollow"', '')
        )

        messages = [FakeMessage("hello\nthere", "error")]
        res = render_template(
            '{% bootstrap_messages messages %}', messages=messages)
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello<br/>there
    </div>
        """
        self.assertEqual(
            re.sub(pattern, '', res),
            re.sub(pattern, '', expected)
        )


class UtilsTest(TestCase):
    def test_add_css_class(self):
        css_classes = "one two"
        css_class = "three four"
        classes = add_css_class(css_classes, css_class)
        self.assertEqual(classes, "one two three four")

        classes = add_css_class(css_classes, css_class, prepend=True)
        self.assertEqual(classes, "three four one two")

    def test_text_value(self):
        self.assertEqual(text_value(''), "")
        self.assertEqual(text_value(' '), " ")
        self.assertEqual(text_value(None), "")
        self.assertEqual(text_value(1), "1")

    def test_text_concat(self):
        self.assertEqual(text_concat(1, 2), "12")
        self.assertEqual(text_concat(1, 2, separator='='), "1=2")
        self.assertEqual(text_concat(None, 2, separator='='), "2")

    def test_render_tag(self):
        self.assertEqual(render_tag('span'), '<span></span>')
        self.assertEqual(render_tag('span', content='foo'), '<span>foo</span>')
        self.assertEqual(
            render_tag('span', attrs={'bar': 123}, content='foo'),
            '<span bar="123">foo</span>'
        )


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

    def test_button_with_icon(self):
        res = render_template(
            "{% bootstrap_button 'test' icon='info-sign' %}"
        )
        self.assertEqual(
            res.strip(),
            '<button class="btn"><span class="glyphicon glyphicon-info-sign"></span> test</button>'
        )

# ############
# Layout tests
# ############

class TestLayoutElement(TestCase):
    def setUp(self):
        self.form = TestForm()
        self.renderer = LayoutFormRenderer(self.form)

    def test_abstract_functions(self):
        self.assertRaises(NotImplementedError, lambda : LayoutElement.from_base_type(""))
        self.assertRaises(NotImplementedError, lambda : LayoutElement()._render(self.form, self.renderer))

    def test_falback_get_natural_child(self):
        well = WellLayoutElement("subject")
        self.assertIsInstance(well._children[0], FieldContainer)
        result = well.render(self.form, self.renderer)
        self.assertEqual(result, '<div class="well">%s</div>' % render_form_field("subject", form=self.form))

    def test_bad_usage_of_get_natural_child(self):
        self.assertRaises(TypeError, lambda : Row().get_natural_children([], {Col(): 2})) # should not pass a LayoutElement to kwargs
        c = Col()
        self.assertIs(LayoutElement().get_natural_child(c), c) # nothing done to a already LayoutElement

    def test_add_child(self):
        c = Col()
        c.add_child("secret")
        c.add_child(FieldContainer("message"))
        l = Layout(Row(c))
        self.assertEqual(list(l.get_children_fields()), ["secret", "message"])

class TestFieldContainer(TestCase):
    def setUp(self):
        self.form = TestForm()
        self.renderer = LayoutFormRenderer(self.form)

    def test_from_base_type(self):
        element = FieldContainer.from_base_type("subject")
        self.assertIsInstance(element, FieldContainer)
        self.assertFalse(element.is_empty(self.form))
        result = element.render(self.form, self.renderer)
        self.assertEqual(result, render_form_field("subject", form=self.form))

    def test_render_all_field(self):
        for f_name in self.form.fields:
            field_alone = render_form_field(f_name, form=self.form)
            element = FieldContainer.from_base_type(f_name)
            self.assertFalse(element.is_empty(self.form))
            fieldcontainen_rendered = element.render(self.form, self.renderer)
            self.assertEqual(field_alone, fieldcontainen_rendered)

    def test_empty(self):
        element = FieldContainer.from_base_type("dontexists")
        self.assertIsInstance(element, FieldContainer)
        result = element.render(self.form, self.renderer)
        self.assertTrue(element.is_empty(self.form))
        self.assertEqual(result, "", "absent field should render nothing")

    def test_get_natural_child(self):
        from .layout import unicode
        # FieldContainer should not have any natural child
        for t in (list, unicode, tuple):
            self.assertRaises(BootstrapException, lambda : FieldContainer("subject").get_natural_child(t()))

    def test_repr(self):
        self.assertEqual(repr(FieldContainer('subject')), str("FieldContainer('subject')"))

    def test_bad_type(self):
        self.assertRaises(TypeError, lambda : FieldContainer.from_base_type(self.form))


class TestCol(TestCase):
    def setUp(self):
        self.form = TestForm()
        self.renderer = LayoutFormRenderer(self.form)

    def test_from_base_type_unicode(self):
        element = Col.from_base_type("subject")
        self.assertIsInstance(element, Col)
        self.assertFalse(element.is_empty(self.form))
        result = element.render(self.form, self.renderer)
        self.assertEqual(result, '<div class="col-md-12">%s</div>' % render_form_field("subject", form=self.form))

    def test_from_base_type_list(self):
        element = Col.from_base_type([FieldContainer("subject")])
        self.assertIsInstance(element, Col)
        self.assertFalse(element.is_empty(self.form))
        result = element.render(self.form, self.renderer)
        self.assertEqual(result, '<div class="col-md-12">%s</div>' % render_form_field("subject", form=self.form))

    def test_empty(self):
        element = Col()
        result = element.render(self.form, self.renderer)
        self.assertTrue(element.is_empty(self.form))
        self.assertEqual(result, '<div class="col-md-12"></div>')

    def test_empty_sub(self):
        element = Col.from_base_type("dontexists")
        self.assertIsInstance(element, Col)
        result = element.render(self.form, self.renderer)
        self.assertTrue(element.is_empty(self.form))
        self.assertEqual(result, '<div class="col-md-12"></div>')

    def test_get_natural_child(self):
        from .layout import unicode
        # FieldContainer should not have any natural child
        for t, expected in ((list, Row), (unicode, FieldContainer), (tuple, Row)):
            self.assertIsInstance(Col().get_natural_child(t()), expected)

    def test_repr(self):
        self.assertEqual(repr(Col(FieldContainer('subject'))), str("Col(FieldContainer('subject'))"))
        self.assertEqual(repr(Col(FieldContainer('subject'), FieldContainer('subject'))), str("Col(FieldContainer('subject'), FieldContainer('subject'))"))

    def test_given_size_base_type(self):
        element = Col.from_base_type("subject", 2)
        self.assertIsInstance(element, Col)
        self.assertFalse(element.is_empty(self.form))
        result = element.render(self.form, self.renderer)
        self.assertEqual(result, '<div class="col-md-2">%s</div>' % render_form_field("subject", form=self.form))

    def test_given_size_by_cfg(self):
        element = Col.from_base_type("subject", dict(size=2))
        self.assertIsInstance(element, Col)
        self.assertFalse(element.is_empty(self.form))
        result = element.render(self.form, self.renderer)
        self.assertEqual(result, '<div class="col-md-2">%s</div>' % render_form_field("subject", form=self.form))

    def test_given_size(self):
        element = Col(FieldContainer("subject"), size=2)
        self.assertIsInstance(element, Col)
        self.assertFalse(element.is_empty(self.form))
        result = element.render(self.form, self.renderer)
        self.assertEqual(result, '<div class="col-md-2">%s</div>' % render_form_field("subject", form=self.form))

    def test_type_error(self):
        self.assertRaises(TypeError, lambda : Col.from_base_type(self.form)) # create Col with form can't be handled


class TestRow(TestCase):
    def setUp(self):
        self.form = TestForm()
        self.renderer = LayoutFormRenderer(self.form)

    def test_from_base_type_unicode(self):
        element = Row.from_base_type("subject")
        self.assertIsInstance(element, Row)
        self.assertFalse(element.is_empty(self.form))
        result = element.render(self.form, self.renderer)
        self.assertEqual(result, '<div class="row"><div class="col-md-12">%s</div></div>' % render_form_field("subject", form=self.form))

    def test_from_base_type_list(self):
        element = Row.from_base_type([Col(FieldContainer("subject"))])
        self.assertIsInstance(element, Row)
        self.assertFalse(element.is_empty(self.form))
        result = element.render(self.form, self.renderer)
        self.assertEqual(result, '<div class="row"><div class="col-md-12">%s</div></div>' % render_form_field("subject", form=self.form))

    def test_form_bad_type(self):
        self.assertRaises(TypeError, lambda : Row.from_base_type(self.form)) # create Col with form can't be handled

    def test_space_reserverd_for_absent_field(self):
        element = Row.from_base_type(["subject", "absent", "message"])
        result = element.render(self.form, self.renderer)
        self.assertEqual(result, '<div class="row"><div class="col-md-4">%s</div>\n<div class="col-md-4"></div>\n<div class="col-md-4">%s</div></div>' % (
            render_form_field("subject", form=self.form),
            render_form_field("message", form=self.form)
        ))

    def test_space_reserved_for_hidden_field(self):
        # since we con't know if the field will be hidden or not at
        # compilation time, we can't compute the row size correctly.
        # hidden fields must be added with size=0 or directly in the layout root
        element = Row.from_base_type(["subject", "secret", "message"])
        result = element.render(self.form, self.renderer)
        self.assertEqual(result, '<div class="row"><div class="col-md-4">%s</div>\n<div class="col-md-4">%s</div>\n<div class="col-md-4">%s</div></div>' % (
            render_form_field("subject", form=self.form),
            render_form_field("secret", form=self.form),
            render_form_field("message", form=self.form)
        ))

    def test_empty(self):
        element = Row()
        result = element.render(self.form, self.renderer)
        self.assertTrue(element.is_empty(self.form))
        self.assertEqual(result, "")

    def test_empty_sub(self):
        element = Row.from_base_type("dontexists")
        self.assertIsInstance(element, Row)
        result = element.render(self.form, self.renderer)
        self.assertTrue(element.is_empty(self.form))
        self.assertEqual(result, "")

    def test_get_natural_child(self):
        from .layout import unicode
        # FieldContainer should not have any natural child
        for t, expected in ((list, Col), (unicode, Col), (tuple, Col)):
            self.assertIsInstance(Row().get_natural_child(t()), expected)

    def test_repr(self):
        self.assertEqual(repr(Col(FieldContainer('subject'))), str("Col(FieldContainer('subject'))"))
        self.assertEqual(repr(Col(FieldContainer('subject'), FieldContainer('message'))), str("Col(FieldContainer('subject'), FieldContainer('message'))"))

    def test_col_size_default(self):
        r = Row("subject","message")
        for child in r._children:
            self.assertIsInstance(child, Col)
            self.assertEqual(child.size, 6)

    def test_space_computing(self):
        # one given, others without space left
        r = Row(Col("subject", size=4), Col("message"), Col("date"))
        self.assertEqual([4, 4, 4], [c.size for c in r._children])
        # one given, but 1 extra space left
        r = Row(Col("subject", size=5), Col("message"), Col("date"))
        self.assertEqual([5, 4, 3], [c.size for c in r._children])
        # two given
        r = Row(Col("subject", size=5), Col("message", size=5), Col("date"))
        self.assertEqual([5, 5, 2], [c.size for c in r._children])
        # no space left for the 2 fields
        with self.assertRaises(BootstrapException):
            Row(Col("subject", size=11), Col("message"), Col("date"))
        # wrong total
        with self.assertRaises(BootstrapException):
            Row(Col("subject", size=5), Col("message", size=5), Col("date", size=3))

    def test_cfg_col_creation(self):
        r = Row(Col("subject", size=4), message=4, date=3)
        # the usage of kwargs mean no order can be preserved.
        self.assertEqual(["date", "message", "subject"], sorted([c._children[0].fieldname for c in r._children]))
        self.assertEqual([3, 4, 4], sorted([c.size for c in r._children]))

    def test_cfg_col_creation_with_order(self):
        r = Row(Col("subject", size=4), "message", "date", message=4, date=3)
        # if the kwarg repeate *args, so it is just the config, and then the order is preserved
        self.assertEqual(["subject", "message", "date"], [c._children[0].fieldname for c in r._children])
        self.assertEqual([4, 4, 3], [c.size for c in r._children])

    def test_add_child(self):
        r = Row("subject")
        # impossible to add in a row because the Row compute
        # each col size at creation.
        with self.assertRaises(BootstrapException):
            r.add_child(Col(FieldContainer("message")))


class EllipsisFieldContainerTest(TestCase):
    def test_is_empty_true(self):
        form = TestForm()
        fields = list(form.fields.keys())
        e = EllipsisFieldContainer()
        fields.append(e)
        l = Layout(*fields)
        self.assertTrue(e.is_empty(form))

    def test_orphan(self):
        form = TestForm()
        renderer = LayoutFormRenderer(form)
        e = EllipsisFieldContainer()
        self.assertTrue(e.is_empty(form))
        self.assertEqual("", e.render(form, renderer))

    def test_is_empty_false(self):
        form = TestForm()
        fields = list()
        e = EllipsisFieldContainer()
        fields.append(e)
        l = Layout(*fields)
        self.assertFalse(e.is_empty(form))

    def test_is_uniq(self):
        l = Layout("subject", "message")
        with self.assertRaises(BootstrapException):
            l.add_child(EllipsisFieldContainer())

    def test_auto_add(self):
        l = Layout("subject", "message")
        self.assertEqual(len(l._children), 3)
        self.assertIsInstance(l._children[-1], EllipsisFieldContainer)

    def test_ellipsis_from_base_type(self):
        # only in python 3 :
        #l = Layout("subject", ..., "message", )
        l = Layout("subject", Ellipsis, "message")
        self.assertIsInstance(l._children[1], EllipsisFieldContainer)

    def test_manual_added(self):
        form = TestForm()
        renderer = LayoutFormRenderer(form)
        efc = EllipsisFieldContainer()
        l = Layout(("subject", "message"), (efc,))
        self.assertIs(efc, l.context["EllipsisFieldContainer"])
        self.assertEqual(2, len(l._children))


class LayoutTest(TestCase):
    def setUp(self):
        self.form = TestForm()
        self.renderer = LayoutFormRenderer(self.form)

    def test_empty_layout(self):
        l = Layout.from_base_type([])
        self.assertFalse(l.is_empty(self.form))
        self.assertTrue(l.is_empty(Form()))

    def test_from_unicode(self):
        fields = [
            "subject",
            "message",
            "date",
        ]
        l = Layout.from_base_type(fields)
        result = l.render(self.form, self.renderer)
        self.assertEqual(
            l.get_missings_fields(self.form),
            ['datetime', 'password', 'sender', 'secret', 'cc_myself', 'select1', 'select2', 'select3', 'select4', 'category1', 'category2', 'category3', 'category4', 'addon']
        )
        self.assertEqual(
            "\n".join((
                render_form_field(name, form=self.form)
                for name in fields + [f for f in self.form.fields if not f in fields] # all fields, but first the choosen ones
            )),
            result
        )

    def test_bad_type(self):
        self.assertRaises(TypeError, lambda : Layout.from_base_type(self.form))

    def test_get_missing_fields(self):
        l = Layout("subject", "message", "date", "missing_field")
        self.assertEqual(
            ['datetime', 'password', 'sender', 'secret', 'cc_myself', 'select1', 'select2', 'select3', 'select4', 'category1', 'category2', 'category3', 'category4', 'addon'],
            list(l.get_missings_fields(TestForm()))
        )

class LayoutFormRendererTest(TestCase):

    def test_get_default_layout(self):
        renderer = LayoutFormRenderer(TestForm())
        layout = renderer.get_layout()
        # take into acount the Ellipsis
        for child in layout._children[:-1]:
            self.assertIsInstance(child, FieldContainer)
        self.assertEqual(len(layout._children), len(renderer.form.fields) + 1)

    def test_get_layout_by_get_layout(self):
        OtherTestForm = type(str("OtherTestForm"), (TestForm, ), {"get_layout": lambda self: Layout("secret")})
        renderer = LayoutFormRenderer(OtherTestForm())
        layout = renderer.get_layout()
        self.assertEqual(len(layout._children), 2) # take into acount the Ellipsis
        self.assertEqual(layout._children[0].fieldname, "secret")

    def test_get_layout_by_fields_layout(self):
        OtherTestForm = type(str("OtherTestForm"), (TestForm, ), {"fields_layout": Layout("secret")})
        renderer = LayoutFormRenderer(OtherTestForm())
        layout = renderer.get_layout()
        self.assertEqual(len(layout._children), 2) # take into acount the Ellipsis
        self.assertEqual(layout._children[0].fieldname, "secret")

    def test_get_layout_from_base_type(self):
        OtherTestForm = type(str("OtherTestForm"), (TestForm, ), {"fields_layout": ("secret",)})
        renderer = LayoutFormRenderer(OtherTestForm())
        layout = renderer.get_layout()
        self.assertEqual(len(layout._children), 2) # take into acount the Ellipsis
        self.assertEqual(layout._children[0].fieldname, "secret")

    def test_render(self):
        form = TestForm()
        renderer = LayoutFormRenderer(form)
        rendered = renderer.render()
        self.assertEqual(render_form(form), rendered)
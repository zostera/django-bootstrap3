# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.widgets import AdminFileWidget
from django.forms import HiddenInput, FileInput, CheckboxSelectMultiple, Textarea, TextInput, DateInput, Select
from django.forms.formsets import BaseFormSet
from django.utils.encoding import force_text

from .bootstrap import get_bootstrap_setting, get_form_renderer, get_field_renderer
from .text import text_concat
from .exceptions import BootstrapError
from .html import add_css_class, render_tag
from .icons import render_icon


FORM_GROUP_CLASS = 'form-group'


def render_formset(formset, **kwargs):
    """
    Render a formset to a Bootstrap layout
    """
    if not isinstance(formset, BaseFormSet):
        raise BootstrapError('Parameter "formset" should contain a valid Django FormSet.')
    forms = [render_form(f, **kwargs) for f in formset]
    return force_text(formset.management_form) + '\n' + '\n'.join(forms)


def render_form(form, layout='', **kwargs):
    """
    Render a formset to a Bootstrap layout
    """
    renderer_cls = get_form_renderer(layout)
    return renderer_cls(form, layout, **kwargs).render()


def render_field(field, layout='', **kwargs):
    """
    Render a formset to a Bootstrap layout
    """
    renderer_cls = get_field_renderer(layout)
    return renderer_cls(field, layout, **kwargs).render()


def render_label(content, label_for=None, label_class=None, label_title=''):
    """
    Render a label with content
    """
    attrs = {}
    if label_for:
        attrs['for'] = label_for
    if label_class:
        attrs['class'] = label_class
    if label_title:
        attrs['title'] = label_title
    return render_tag('label', attrs=attrs, content=content)


def render_button(content, button_type=None, icon=None):
    """
    Render a button with content
    """
    attrs = {'class': 'btn'}
    if button_type:
        if button_type == 'submit':
            attrs['class'] += ' btn-primary'
        elif button_type != 'reset' and button_type != 'button':
            raise BootstrapError('Parameter "button_type" should be "submit", "reset", "button" or empty.')
        attrs['type'] = button_type
    icon_content = render_icon(icon) if icon else ''
    return render_tag('button', attrs=attrs, content=text_concat(icon_content, content, separator=' '))


def render_field_and_label(field, label, field_class='', label_class='', layout='', **kwargs):
    """
    Render a field with its label
    """
    if layout == 'horizontal':
        if not label_class:
            label_class = get_bootstrap_setting('horizontal_label_class')
        if not field_class:
            field_class = get_bootstrap_setting('horizontal_field_class')
        if not label:
            label = '&#160;'
        label_class = add_css_class(label_class, 'control-label')
    html = field
    if field_class:
        html = '<div class="{klass}">{html}</div>'.format(klass=field_class, html=html)
    if label:
        html = render_label(label, label_class=label_class) + html
    return html


def render_form_group(content, css_class=FORM_GROUP_CLASS):
    """
    Render a Bootstrap form group
    """
    return '<div class="{klass}">{content}</div>'.format(
        klass=css_class,
        content=content,
    )


def is_widget_required_attribute(widget):
    """
    Is this widget required?
    """
    if not get_bootstrap_setting('set_required'):
        return False
    if not widget.is_required:
        return False
    if isinstance(widget, (AdminFileWidget, HiddenInput, FileInput, CheckboxSelectMultiple)):
        return False
    return True


def is_widget_with_placeholder(widget):
    """
    Is this a widget that should have a placeholder?
    Only text, search, url, tel, e-mail, password, number have placeholders
    These are all derived form TextInput, except for Textarea
    """
    return isinstance(widget, (TextInput, Textarea))


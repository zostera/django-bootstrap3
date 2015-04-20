# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.widgets import AdminFileWidget
from django.forms import (
    HiddenInput, FileInput, CheckboxSelectMultiple, Textarea, TextInput,
    PasswordInput
)
from django.forms.widgets import CheckboxInput

from .bootstrap import (
    get_bootstrap_setting, get_form_renderer, get_field_renderer,
    get_formset_renderer
)
from .text import text_concat, text_value
from .exceptions import BootstrapError
from .utils import add_css_class, render_tag, split_css_classes
from .components import render_icon


FORM_GROUP_CLASS = 'form-group'


def render_formset(formset, **kwargs):
    """
    Render a formset to a Bootstrap layout
    """
    renderer_cls = get_formset_renderer(**kwargs)
    return renderer_cls(formset, **kwargs).render()


def render_formset_errors(formset, **kwargs):
    """
    Render formset errors to a Bootstrap layout
    """
    renderer_cls = get_formset_renderer(**kwargs)
    return renderer_cls(formset, **kwargs).render_errors()


def render_form(form, **kwargs):
    """
    Render a form to a Bootstrap layout
    """
    renderer_cls = get_form_renderer(**kwargs)
    return renderer_cls(form, **kwargs).render()


def render_form_errors(form, type='all', **kwargs):
    """
    Render form errors to a Bootstrap layout
    """
    renderer_cls = get_form_renderer(**kwargs)
    return renderer_cls(form, **kwargs).render_errors(type)


def render_field(field, **kwargs):
    """
    Render a field to a Bootstrap layout
    """
    renderer_cls = get_field_renderer(**kwargs)
    return renderer_cls(field, **kwargs).render()


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


def render_button(
        content, button_type=None, icon=None, button_class='', size='',
        href='', name=None, value=None):
    """
    Render a button with content
    """
    attrs = {}
    classes = add_css_class('btn', button_class)
    size = text_value(size).lower().strip()
    if size == 'xs':
        classes = add_css_class(classes, 'btn-xs')
    elif size == 'sm' or size == 'small':
        classes = add_css_class(classes, 'btn-sm')
    elif size == 'lg' or size == 'large':
        classes = add_css_class(classes, 'btn-lg')
    elif size == 'md' or size == 'medium':
        pass
    elif size:
        raise BootstrapError(
            'Parameter "size" should be "xs", "sm", "lg" or ' +
            'empty ("{}" given).'.format(size))
    if button_type:
        if button_type == 'submit':
            if not any([c.startswith('btn-') for c in split_css_classes(classes)]):
                classes = add_css_class(classes, 'btn-primary')
        elif button_type not in ('reset', 'button', 'link'):
            raise BootstrapError(
                'Parameter "button_type" should be "submit", "reset", ' +
                '"button", "link" or empty  ("{}" given).'.format(button_type))
        attrs['type'] = button_type
    attrs['class'] = classes
    icon_content = render_icon(icon) if icon else ''
    if href:
        attrs['href'] = href
        tag = 'a'
    else:
        tag = 'button'
    if name:
        attrs['name'] = name
    if value:
        attrs['value'] = value
    return render_tag(
        tag, attrs=attrs, content=text_concat(
            icon_content, content, separator=' '))


def render_field_and_label(
        field, label, field_class='', label_for=None, label_class='',
        layout='', **kwargs):
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
        html = '<div class="{klass}">{html}</div>'.format(
            klass=field_class, html=html)
    if label:
        html = render_label(
            label, label_for=label_for, label_class=label_class) + html
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
    if isinstance(
            widget, (
                AdminFileWidget, HiddenInput, FileInput,
                CheckboxInput, CheckboxSelectMultiple)):
        return False
    return True


def is_widget_with_placeholder(widget):
    """
    Is this a widget that should have a placeholder?
    Only text, search, url, tel, e-mail, password, number have placeholders
    These are all derived form TextInput, except for Textarea
    """
    # PasswordInput inherits from Input in Django 1.4.
    # It was changed to inherit from TextInput in 1.5.
    return isinstance(widget, (TextInput, Textarea, PasswordInput))

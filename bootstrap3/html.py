# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms.widgets import flatatt

from .text import force_text, text_value


# Handle HTML and CSS manipulation


def split_css_classes(css_classes):
    """
    Turn string into a list of CSS classes
    """
    classes_list = force_text(css_classes).split(' ')
    return [c for c in classes_list if c]


def add_css_class(css_classes, css_class):
    """
    Add a CSS class to a string of CSS classes
    """
    classes_list = split_css_classes(css_classes)
    for c in split_css_classes(css_class):
        if c not in classes_list:
            classes_list.append(c)
    return ' '.join(classes_list)


def remove_css_class(css_classes, css_class):
    """
    Remove a CSS class from a string of CSS classes
    """
    remove = set(split_css_classes(css_class))
    classes_list = [c for c in split_css_classes(css_classes) if c not in remove]
    return ' '.join(classes_list)


def render_link_tag(url, rel='stylesheet', media='all'):
    """
    Build a link tag
    """
    return render_tag('link', attrs = {'href': url, 'rel': rel, 'media': media}, close=False)


def render_tag(tag, attrs=None, content=None, close=True):
    """
    Render a HTML tag
    """
    builder = '<{tag}{attrs}>{content}'
    if content or close:
        builder += '</{tag}>'
    return builder.format(
        tag=tag,
        attrs=flatatt(attrs) if attrs else '',
        content=text_value(content),
    )

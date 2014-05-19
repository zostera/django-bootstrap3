# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.utils.importlib import import_module


# Default settings
BOOTSTRAP3_DEFAULTS = {
    'jquery_url': '//code.jquery.com/jquery.min.js',
    'base_url': '//netdna.bootstrapcdn.com/bootstrap/3.1.1/',
    'css_url': None,
    'theme_url': None,
    'javascript_url': None,
    'javascript_in_head': False,
    'include_jquery': False,
    'horizontal_label_class': 'col-md-2',
    'horizontal_field_class': 'col-md-4',
    'set_required': True,
    'form_required_class': '',
    'form_error_class': '',
    'form_renderers': {
        'default': 'bootstrap3.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },
    'error_line_break': False,
    'error_icon': None
}

# Start with a copy of default settings
BOOTSTRAP3 = BOOTSTRAP3_DEFAULTS.copy()

# Override with user settings from settings.py
BOOTSTRAP3.update(getattr(settings, 'BOOTSTRAP3', {}))


def get_bootstrap_setting(setting, default=None):
    """
    Read a setting
    """
    return BOOTSTRAP3.get(setting, default)


def bootstrap_url(postfix):
    """
    Prefix a relative url with the bootstrap base url
    """
    return get_bootstrap_setting('base_url') + postfix


def jquery_url():
    """
    Return the full url to jQuery file to use
    """
    return get_bootstrap_setting('jquery_url')


def javascript_url():
    """
    Return the full url to the Bootstrap JavaScript file
    """
    return get_bootstrap_setting('javascript_url') or bootstrap_url('js/bootstrap.min.js')


def css_url():
    """
    Return the full url to the Bootstrap CSS file
    """
    return get_bootstrap_setting('css_url') or bootstrap_url('css/bootstrap.min.css')


def theme_url():
    """
    Return the full url to the theme CSS file
    """
    return get_bootstrap_setting('theme_url')


def get_renderer(renderers, layout):
    path = renderers.get(layout, renderers['default'])
    mod, cls = path.rsplit(".", 1)
    return getattr(import_module(mod), cls)


def get_form_renderer(layout):
    renderers = get_bootstrap_setting('form_renderers')
    return get_renderer(renderers, layout)


def get_field_renderer(layout):
    renderers = get_bootstrap_setting('field_renderers')
    return get_renderer(renderers, layout)


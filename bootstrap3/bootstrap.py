# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings

# Default settings
BOOTSTRAP3_DEFAULTS = {
    'jquery_url': '//code.jquery.com/jquery.min.js',
    'base_url': '//netdna.bootstrapcdn.com/bootstrap/3.0.3/',
    'css_url': None,
    'theme_url': None,
    'javascript_url': None,
    'horizontal_label_class': 'col-md-2',
    'horizontal_field_class': 'col-md-4',
}

# Start with a copy of default settings
BOOTSTRAP3 = BOOTSTRAP3_DEFAULTS.copy()

# Override with user settings from settings.py
BOOTSTRAP3.update(getattr(settings, 'BOOTSTRAP3', {}))


def bootstrap_url(postfix):
    """
    Prefix a relative url with the bootstrap base url
    """
    return BOOTSTRAP3['base_url'] + postfix


def jquery_url():
    """
    Return the full url to jQuery file to use
    """
    return BOOTSTRAP3['jquery_url']


def javascript_url():
    """
    Return the full url to the Bootstrap JavaScript file
    """
    return BOOTSTRAP3['javascript_url'] or bootstrap_url('js/bootstrap.min.js')


def css_url():
    """
    Return the full url to the Bootstrap CSS file
    """
    return BOOTSTRAP3['css_url'] or bootstrap_url('css/bootstrap.min.css')

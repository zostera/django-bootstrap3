# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from importlib import import_module

from django import VERSION as DJANGO_VERSION
from django.conf import settings

# Default settings
BOOTSTRAP3_DEFAULTS = {
    "css_url": {
        "url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css",
        "integrity": "sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u",
        "crossorigin": "anonymous",
    },
    "theme_url": None,
    "javascript_url": {
        "url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js",
        "integrity": "sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa",
        "crossorigin": "anonymous",
    },
    "jquery_url": "//code.jquery.com/jquery.min.js",
    "javascript_in_head": False,
    "include_jquery": False,
    "horizontal_label_class": "col-md-3",
    "horizontal_field_class": "col-md-9",
    "set_placeholder": True,
    "required_css_class": "",
    "error_css_class": "has-error",
    "success_css_class": "has-success",
    "formset_renderers": {"default": "bootstrap3.renderers.FormsetRenderer"},
    "form_renderers": {"default": "bootstrap3.renderers.FormRenderer"},
    "field_renderers": {
        "default": "bootstrap3.renderers.FieldRenderer",
        "inline": "bootstrap3.renderers.InlineFieldRenderer",
    },
}

# Start with a copy of default settings
BOOTSTRAP3 = BOOTSTRAP3_DEFAULTS.copy()

# Override with user settings from settings.py
BOOTSTRAP3.update(getattr(settings, "BOOTSTRAP3", {}))


def get_bootstrap_setting(setting, default=None):
    """
    Read a setting
    """
    return BOOTSTRAP3.get(setting, default)


def jquery_url():
    """
    Return the full url to jQuery file to use
    """
    return get_bootstrap_setting("jquery_url")


def javascript_url():
    """
    Return the full url to the Bootstrap JavaScript file
    """
    return get_bootstrap_setting("javascript_url")


def css_url():
    """
    Return the full url to the Bootstrap CSS file
    """
    return get_bootstrap_setting("css_url")


def theme_url():
    """
    Return the full url to the theme CSS file
    """
    return get_bootstrap_setting("theme_url")


def get_renderer(renderers, **kwargs):
    layout = kwargs.get("layout", "")
    path = renderers.get(layout, renderers["default"])
    mod, cls = path.rsplit(".", 1)
    return getattr(import_module(mod), cls)


def get_formset_renderer(**kwargs):
    renderers = get_bootstrap_setting("formset_renderers")
    return get_renderer(renderers, **kwargs)


def get_form_renderer(**kwargs):
    renderers = get_bootstrap_setting("form_renderers")
    return get_renderer(renderers, **kwargs)


def get_field_renderer(**kwargs):
    renderers = get_bootstrap_setting("field_renderers")
    return get_renderer(renderers, **kwargs)

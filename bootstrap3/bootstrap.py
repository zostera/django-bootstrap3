# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module


# Default settings
BOOTSTRAP3_DEFAULTS = {
    'jquery_url': '//code.jquery.com/jquery.min.js',
    #'jquery_url': '//code.jquery.com/jquery-1.12.0.min.js',
	'jquery_integrity': None,
    'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/',
    'css_url': None,
	'css_integrity': None,
    'theme_url': None,
	'theme_integrity': None,
    'javascript_url': None,
	'javascript_integrity': None,
    'javascript_in_head': False,
    'include_jquery': False,
    'horizontal_label_class': 'col-md-3',
    'horizontal_field_class': 'col-md-9',
    'set_required': True,
    'set_disabled': False,
    'set_placeholder': True,
    'required_css_class': '',
    'error_css_class': 'has-error',
    'success_css_class': 'has-success',
    'formset_renderers': {
        'default': 'bootstrap3.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'bootstrap3.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },
}

# Provides integrity values for pointed default version - https://www.srihash.org/ used
BOOTSTRAP3_DEFAULT_INTEGRITY = {
	'jquery': 'sha384-omOsxWjfyCQN/QkJa5gsN9F1sKX/IRXsLKvv7uHdTUYqkonYl4B/SrIIrNmrnJDj', # 1.11.0 'jquery.min.js'
	#'jquery': 'sha384-XxcvoeNF5V0ZfksTnV+bejnCsJjOOIzN6UVwF85WBsAnU3zeYh5bloN+L4WLgeNE', # 1.12.0-min
	'javascript': 'sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS', # js/bootstrap.min.js
	'css': 'sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7', # css/bootstrap.min.css
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


def jquery_integrity():
	"""
    Return the integrity tag value of jQuery file if provided or default version if used
    """
	if get_bootstrap_setting('jquery_integrity'):
		return get_bootstrap_setting('jquery_integrity')
	elif get_bootstrap_setting('jquery_url') == BOOTSTRAP3_DEFAULTS.get('jquery_url'):
		return BOOTSTRAP3_DEFAULT_INTEGRITY.get('jquery', None)
	else:
		return None


def javascript_url():
    """
    Return the full url to the Bootstrap JavaScript file
    """
    return get_bootstrap_setting('javascript_url') or \
        bootstrap_url('js/bootstrap.min.js')


def javascript_integrity():
    """
    Return the integrity tag value of JavaScript file if provided or default version if used
    """
	if get_bootstrap_setting('javascript_integrity'):
		return get_bootstrap_setting('javascript_integrity')
	elif not get_bootstrap_setting('javascript_url'):
		return BOOTSTRAP3_DEFAULT_INTEGRITY.get('javascript', None)
	else:
		return None


def css_url():
    """
    Return the full url to the Bootstrap CSS file
    """
    return get_bootstrap_setting('css_url') or \
        bootstrap_url('css/bootstrap.min.css')


def css_integrity():
    """
    Return the integrity tag value of CSS file if provided or default version if used
    """
	if get_bootstrap_setting('css_integrity'):
		return get_bootstrap_setting('css_integrity')
	elif not get_bootstrap_setting('css_url'):
		return BOOTSTRAP3_DEFAULT_INTEGRITY.get('css', None)
	else:
		return None


def theme_url():
    """
    Return the full url to the theme CSS file
    """
    return get_bootstrap_setting('theme_url')


def theme_integrity():
    """
    Return the integrity tag value of Javascript file if provided or default version if used
    """
	return get_bootstrap_setting('theme_integrity')


def get_renderer(renderers, **kwargs):
    layout = kwargs.get('layout', '')
    path = renderers.get(layout, renderers['default'])
    mod, cls = path.rsplit(".", 1)
    return getattr(import_module(mod), cls)


def get_formset_renderer(**kwargs):
    renderers = get_bootstrap_setting('formset_renderers')
    return get_renderer(renderers, **kwargs)


def get_form_renderer(**kwargs):
    renderers = get_bootstrap_setting('form_renderers')
    return get_renderer(renderers, **kwargs)


def get_field_renderer(**kwargs):
    renderers = get_bootstrap_setting('field_renderers')
    return get_renderer(renderers, **kwargs)

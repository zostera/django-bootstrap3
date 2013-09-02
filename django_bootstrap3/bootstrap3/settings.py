from __future__ import unicode_literals

from django.conf import settings


BOOTSTRAP3_DEFAULTS = {
    'include_jquery': False,
    'jquery_url': '//code.jquery.com/jquery.min.js',
    'base_url': '//netdna.bootstrapcdn.com/bootstrap/3.0.0/',
    'css_url': None,
    'theme_url': None,
    'javascript_url': None,
}

BOOTSTRAP3 = getattr(settings, 'BOOTSTRAP3', {})
BOOTSTRAP3.update(BOOTSTRAP3_DEFAULTS)


def bootstrap_url(postfix):
    return BOOTSTRAP3['base_url'] + postfix


def jquery_url():
    if BOOTSTRAP3['include_jquery']:
        return BOOTSTRAP3['jquery_url']
    return ''


def javascript_url():
    return BOOTSTRAP3['javascript_url'] or bootstrap_url('js/bootstrap.min.js')


def css_url():
    return BOOTSTRAP3['css_url'] or bootstrap_url('css/bootstrap.min.css')

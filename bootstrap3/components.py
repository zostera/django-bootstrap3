# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms.widgets import flatatt

from .text import text_value


def render_icon(icon, title=''):
    """
    Render a Bootstrap glyphicon icon
    """
    attrs = {
        'class': 'glyphicon glyphicon-{icon}'.format(icon=icon),
    }
    if title:
        attrs['title'] = title
    return '<span{attrs}></span>'.format(attrs=flatatt(attrs))


def render_alert(content, alert_type=None, dismissable=True):
    """
    Render a Bootstrap alert
    """
    button = ''
    if not alert_type:
        alert_type = 'info'
    css_classes = ['alert', 'alert-' + text_value(alert_type)]
    if dismissable:
        css_classes.append('alert-dismissable')
        button = '<button type="button" class="close" ' + \
                 'data-dismiss="alert" aria-hidden="true">&times;</button>'
    return '<div class="{css_classes}">{button}{content}</div>'.format(
        css_classes=' '.join(css_classes),
        button=button,
        content=text_value(content),
    )

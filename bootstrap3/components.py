# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms.widgets import flatatt
from django.utils.safestring import mark_safe
from bootstrap3.utils import render_tag

from .text import text_value


def render_icon(icon, **kwargs):
    """
    Render a Bootstrap glyphicon icon
    """
    classes = ['glyphicon glyphicon-{icon}'.format(icon=icon)]
    if kwargs.get('add_class'):
        classes.append(kwargs.get('add_class'))
    attrs = {
        'class': ' '.join(classes),
    }
    if kwargs.get('title'):
        attrs['title'] = kwargs.get('title')

    return render_tag('span', attrs=attrs)


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
    button_placeholder = '__BUTTON__'
    return mark_safe(render_tag(
        'div',
        attrs={'class': ' '.join(css_classes)},
        content=button_placeholder + text_value(content),
    ).replace(button_placeholder, button))

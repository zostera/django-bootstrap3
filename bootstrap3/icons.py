# -*- coding: utf-8 -*-
from __future__ import unicode_literals

def render_icon(icon):
    """
    Render a Bootstrap glyphicon icon
    """
    return '<span class="glyphicon glyphicon-{icon}"></span>'.format(icon=icon)

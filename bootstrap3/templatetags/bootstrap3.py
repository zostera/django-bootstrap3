from __future__ import absolute_import
from __future__ import unicode_literals

from django import template

from ..bootstrap import jquery_url, javascript_url, css_url
from ..icons import render_icon
from ..forms import render_formset, render_field, render_form, render_button, render_label, render_form_group, render_field_and_label
from ..templates import parse_token_contents, handle_var


register = template.Library()


@register.simple_tag
def bootstrap_jquery_url():
    return jquery_url()


@register.simple_tag
def bootstrap_javascript_url():
    return javascript_url()


@register.simple_tag
def bootstrap_css_url():
    return css_url()


@register.simple_tag
def bootstrap_css():
    url = bootstrap_css_url()
    if url:
        return '<link href="%s" rel="stylesheet" media="screen">' % url
    return ''


@register.simple_tag
def bootstrap_javascript(jquery=False):
    javascript = ''
    if jquery:
        url = bootstrap_jquery_url()
        if url:
            javascript += '<script src="%s"></script>' % url
    url = bootstrap_javascript_url()
    if url:
        javascript += '<script src="%s"></script>' % url
    return javascript


@register.simple_tag
def bootstrap_formset(*args, **kwargs):
    """
    Render a formset
    """
    return render_formset(*args, **kwargs)


@register.simple_tag
def bootstrap_form(*args, **kwargs):
    """
    Render a form
    """
    return render_form(*args, **kwargs)


@register.simple_tag
def bootstrap_field(*args, **kwargs):
    return render_field(*args, **kwargs)


@register.simple_tag()
def bootstrap_label(*args, **kwargs):
    return render_label(*args, **kwargs)


@register.simple_tag
def bootstrap_button(*args, **kwargs):
    return render_button(*args, **kwargs)


@register.simple_tag
def bootstrap_icon(icon):
    """
    Return an icon
    """
    return render_icon(icon)


@register.tag
def bootstrap_form_buttons(parser, token):
    kwargs = parse_token_contents(parser, token)
    kwargs['nodelist'] = parser.parse(('end_bootstrap_form_buttons', ))
    parser.delete_first_token()
    return BootstrapFormButtonsNode(**kwargs)


class BootstrapFormButtonsNode(template.Node):
    def __init__(self, nodelist, args, kwargs, asvar, **kwargs2):
        self.nodelist = nodelist
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        kwargs = {}
        for key in self.kwargs:
            kwargs[key] = handle_var(self.kwargs[key], context)
        buttons = []
        submit = kwargs.get('submit', None)
        cancel = kwargs.get('cancel', None)
        if submit:
            buttons.append(bootstrap_button(submit, 'submit'))
        if cancel:
            buttons.append(bootstrap_button(cancel, 'cancel'))
        buttons = ' '.join(buttons) + self.nodelist.render(context)
        kwargs.update({
            'label': None,
            'field': buttons,
        })
        output = render_form_group(render_field_and_label(**kwargs))
        if self.asvar:
            context[self.asvar] = output
            return ''
        else:
            return output
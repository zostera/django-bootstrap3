from math import floor
import re
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

@register.inclusion_tag("bootstrap3/pagination.html")
def bootstrap_pagination(page, **kwargs):
    """
    Render pagination for a page
    """
    pagination_kwargs = kwargs.copy()
    pagination_kwargs['page'] = page
    return get_pagination_context(**pagination_kwargs)


def get_pagination_context(page, pages_to_show=11, url=None, size=None, extra=None):
    """
    Generate Bootstrap pagination context from a page object
    """
    pages_to_show = int(pages_to_show)
    if pages_to_show < 1:
        raise ValueError("Pagination pages_to_show should be a positive integer, you specified %s" % pages_to_show)
    num_pages = page.paginator.num_pages
    current_page = page.number
    half_page_num = int(floor(pages_to_show / 2)) - 1
    if half_page_num < 0:
        half_page_num = 0
    first_page = current_page - half_page_num
    if first_page <= 1:
        first_page = 1
    if first_page > 1:
        pages_back = first_page - half_page_num
        if pages_back < 1:
            pages_back = 1
    else:
        pages_back = None
    last_page = first_page + pages_to_show - 1
    if pages_back is None:
        last_page += 1
    if last_page > num_pages:
        last_page = num_pages
    if last_page < num_pages:
        pages_forward = last_page + half_page_num
        if pages_forward > num_pages:
            pages_forward = num_pages
    else:
        pages_forward = None
        if first_page > 1:
            first_page -= 1
        if pages_back > 1:
            pages_back -= 1
        else:
            pages_back = None
    pages_shown = []
    for i in range(first_page, last_page + 1):
        pages_shown.append(i)
    # Append proper character to url
    if url:
        # Remove existing page GET parameters
        url = unicode(url)
        url = re.sub(r'\?page\=[^\&]+', u'?', url)
        url = re.sub(r'\&page\=[^\&]+', u'', url)
        # Append proper separator
        if u'?' in url:
            url += u'&'
        else:
            url += u'?'
    # Append extra string to url
    if extra:
        if not url:
            url = u'?'
        url += unicode(extra) + u'&'
    if url:
        url = url.replace(u'?&', u'?')
    # Set CSS classes, see http://twitter.github.io/bootstrap/components.html#pagination
    pagination_css_classes = ['pagination']
    if size == 'small':
        pagination_css_classes.append('pagination-sm')
    elif size == 'large':
        pagination_css_classes.append('pagination-lg')
    # Build context object
    return {
        'bootstrap_pagination_url': url,
        'num_pages': num_pages,
        'current_page': current_page,
        'first_page': first_page,
        'last_page': last_page,
        'pages_shown': pages_shown,
        'pages_back': pages_back,
        'pages_forward': pages_forward,
        'pagination_css_classes': ' '.join(pagination_css_classes),
    }

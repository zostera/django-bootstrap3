from __future__ import unicode_literals

import re
from math import floor

from django import template
from django.template.loader import get_template
from django.utils.encoding import force_text

from ..bootstrap import css_url, javascript_url, jquery_url, theme_url
from ..html import link_tag
from ..forms import render_button, render_field, render_field_and_label, render_form, render_form_group, render_formset, \
    render_label
from ..icons import render_icon
from ..templates import handle_var, parse_token_contents

register = template.Library()


@register.simple_tag
def bootstrap_jquery_url():
    """
    **Tag name**::
        
        bootstrap_jquery_url

    Return the full url to jQuery file to use

    Default value: ``//code.jquery.com/jquery.min.js``

    this value is configurable, see Settings section 
    
    **usage**::

        {% bootstrap_jquery_url %}

    **example**::

        {% bootstrap_jquery_url %}
    """
    return jquery_url()


@register.simple_tag
def bootstrap_javascript_url():
    """
    Return the full url to FIXTHIS

    Default value: ``None``

    this value is configurable, see Settings section 

    **Tag name**::
        
        bootstrap_javascript_url
    
    **usage**::
    
        {% bootstrap_javascript_url %}

    **example**::

        {% bootstrap_javascript_url %}
    """
    return javascript_url()


@register.simple_tag
def bootstrap_css_url():
    """
    Return the full url to FIXTHIS

    Default value: ``None``

    this value is configurable, see Settings section 

    **Tag name**::
        
        bootstrap_css_url
    
    **usage**::
    
        {% bootstrap_css_url %}

    **example**::

        {% bootstrap_css_url %}
    """
    return css_url()


@register.simple_tag
def bootstrap_theme_url():
    """
    Return the full url to FIXTHIS

    Default value: ``None``

    this value is configurable, see Settings section

    **Tag name**::

        bootstrap_css_url

    **usage**::

        {% bootstrap_css_url %}

    **example**::

        {% bootstrap_css_url %}
    """
    return theme_url()


@register.simple_tag
def bootstrap_css():
    """
    Return HTML for Bootstrap CSS
    Adjust url in settings. If no url is returned, we don't want this statement to return any HTML.
    This is intended behavior.

    Default value: ``FIXTHIS``

    this value is configurable, see Settings section 

    **Tag name**::
        
        bootstrap_css
    
    **usage**::
    
        {% bootstrap_css %}

    **example**::

        {% bootstrap_css %}
    """
    urls = [url for url in [bootstrap_css_url(), bootstrap_theme_url()] if url]
    return ''.join([link_tag(url, media='screen') for url in urls])


@register.simple_tag
def bootstrap_javascript(jquery=False):
    """
    Return HTML for Bootstrap JavaScript
    Adjust url in settings. If no url is returned, we don't want this statement to return any HTML.
    This is intended behavior.

    Default value: ``None``

    this value is configurable, see Settings section 

    **Tag name**::
        
        bootstrap_javascript

    **Parameters**:
        
        :jquery: True to include jquery FIXTHIS

    **usage**::
    
        {% bootstrap_javascript FIXTHIS %}

    **example**::

        {% bootstrap_javascript FIXTHIS %}
    """

    javascript = ''
    # No async on scripts, not mature enough. See issue #52 and #56
    if jquery:
        url = bootstrap_jquery_url()
        if url:
            javascript += '<script src="{url}"></script>'.format(url=url)
    url = bootstrap_javascript_url()
    if url:
        javascript += '<script src="{url}"></script>'.format(url=url)
    return javascript


@register.simple_tag
def bootstrap_formset(*args, **kwargs):
    """
    Render a formset


    **Tag name**::
        
        bootstrap_formset

    **Parameters**:
        
        :args: 
        :kwargs: 
  
    **usage**::
    
        {% bootstrap_formset formset FIXTHIS %}

    **example**::
    
        {% bootstrap_formset formset FIXTHIS %}

    """
    return render_formset(*args, **kwargs)


@register.simple_tag
def bootstrap_form(*args, **kwargs):
    """
    Render a form

    **Tag name**::
        
        bootstrap_form

    **Parameters**:
        
        :args: 
        :kwargs:   

    **usage**::
    
        {% bootstrap_form form FIXTHIS %}

    **example**::
    
        {% bootstrap_form form FIXTHIS %}
    """
    return render_form(*args, **kwargs)


@register.simple_tag
def bootstrap_field(*args, **kwargs):
    """
    Render a field

    **Tag name**::
        
        bootstrap_field

    **Parameters**:
        
        :args: 
        :kwargs:   

    **usage**::
    
        {% bootstrap_field form_field FIXTHIS %}

    **example**::
    
        {% bootstrap_form form_field FIXTHIS %}
    """
    return render_field(*args, **kwargs)


@register.simple_tag()
def bootstrap_label(*args, **kwargs):
    """
    Render a label

    **Tag name**::
        
        bootstrap_label

    **Parameters**:
        
        :args: 
        :kwargs:      

    **usage**::
    
        {% bootstrap_label FIXTHIS %}

    **example**::
    
        {% bootstrap_label FIXTHIS %}
    """
    return render_label(*args, **kwargs)


@register.simple_tag
def bootstrap_button(*args, **kwargs):
    """
    Render a button

    **Tag name**::
        
        bootstrap_button

    **Parameters**:
        
        :args: 
        :kwargs:     

    **usage**::
    
        {% bootstrap_button FIXTHIS %}

    **example**::
    
        {% bootstrap_button FIXTHIS %}
    """
    return render_button(*args, **kwargs)


@register.simple_tag
def bootstrap_icon(icon):
    """
    Render an icon

    **Tag name**::
        
        bootstrap_icon

    **Parameters**:
        
        :icon: icon name

    **usage**::
    
        {% bootstrap_icon "icon_name" %}

    **example**::
    
        {% bootstrap_icon "star" %}

    """
    return render_icon(icon)


@register.tag('buttons')
def bootstrap_buttons(parser, token):
    """
    Render buttons for form

    **Tag name**::
        
        bootstrap_buttons

    **Parameters**:
        
        :parser: 
        :token: 

    **usage**::
    
        {% bootstrap_buttons FIXTHIS %}

    **example**::
    
        {% bootstrap_buttons FIXTHIS %}
    """
    kwargs = parse_token_contents(parser, token)
    kwargs['nodelist'] = parser.parse(('endbuttons', ))
    parser.delete_first_token()
    return ButtonsNode(**kwargs)


class ButtonsNode(template.Node):
    def __init__(self, nodelist, args, kwargs, asvar, **kwargs2):
        self.nodelist = nodelist
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        output_kwargs = {}
        for key in self.kwargs:
            output_kwargs[key] = handle_var(self.kwargs[key], context)
        buttons = []
        submit = output_kwargs.get('submit', None)
        reset = output_kwargs.get('reset', None)
        if submit:
            buttons.append(bootstrap_button(submit, 'submit'))
        if reset:
            buttons.append(bootstrap_button(reset, 'reset'))
        buttons = ' '.join(buttons) + self.nodelist.render(context)
        output_kwargs.update({
            'label': None,
            'field': buttons,
        })
        output = render_form_group(render_field_and_label(**output_kwargs))
        if self.asvar:
            context[self.asvar] = output
            return ''
        else:
            return output


@register.simple_tag(takes_context=True)
def bootstrap_messages(context, *args, **kwargs):
    """
    Show django.contrib.messages Messages in Bootstrap alert containers

    **Tag name**::
        
        bootstrap_messages

    **Parameters**:
        
        :context: 
        :args: 
        :kwargs:     

    **usage**::
    
        {% bootstrap_messages FIXTHIS %}

    **example**::
    
        {% bootstrap_messages FIXTHIS %}

   """
    return get_template('bootstrap3/messages.html').render(context)


@register.inclusion_tag('bootstrap3/pagination.html')
def bootstrap_pagination(page, **kwargs):
    """
    Render pagination for a page

    **Tag name**::
        
        bootstrap_pagination

    **Parameters**:
        
        :page: 
        :kwargs:

    **usage**::
    
        {% bootstrap_pagination FIXTHIS %}

    **example**::
    
        {% bootstrap_pagination FIXTHIS %}
    """

    pagination_kwargs = kwargs.copy()
    pagination_kwargs['page'] = page
    return get_pagination_context(**pagination_kwargs)


def get_pagination_context(page, pages_to_show=11,
                           url=None, size=None, extra=None):
    """
    Generate Bootstrap pagination context from a page object
    """
    pages_to_show = int(pages_to_show)
    if pages_to_show < 1:
        raise ValueError("Pagination pages_to_show should be a positive " +
                         "integer, you specified {pages}".format(pages=pages_to_show))
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
        if pages_back is not None and pages_back > 1:
            pages_back -= 1
        else:
            pages_back = None
    pages_shown = []
    for i in range(first_page, last_page + 1):
        pages_shown.append(i)
        # Append proper character to url
    if url:
        # Remove existing page GET parameters
        url = force_text(url)
        url = re.sub(r'\?page\=[^\&]+', '?', url)
        url = re.sub(r'\&page\=[^\&]+', '', url)
        # Append proper separator
        if '?' in url:
            url += '&'
        else:
            url += '?'
            # Append extra string to url
    if extra:
        if not url:
            url = '?'
        url += force_text(extra) + '&'
    if url:
        url = url.replace('?&', '?')
    # Set CSS classes,see twitter.github.io/bootstrap/components.html#pagination
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

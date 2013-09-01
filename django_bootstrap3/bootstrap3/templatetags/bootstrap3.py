from django import template
from django.forms import widgets
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms.widgets import flatatt

from ..utils import add_css_class


FORM_GROUP_CLASS = 'form-group'

register = template.Library()


@register.simple_tag
def bootstrap_jquery_url():
    return '//code.jquery.com/jquery.min.js'


@register.simple_tag
def bootstrap_javascript_url():
    return '//netdna.bootstrapcdn.com/bootstrap/3.0.0-wip/css/bootstrap.min.css'


@register.simple_tag
def bootstrap_css_url():
    return '//netdna.bootstrapcdn.com/bootstrap/3.0.0-wip/js/bootstrap.min.js'


@register.simple_tag
def bootstrap_css():
    url = bootstrap_javascript_url()
    if not url:
        return ''
    return mark_safe('<link href="%s" rel="stylesheet" media="screen">' % url)


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
    return mark_safe(javascript)


@register.simple_tag
def bootstrap_formset(formset, **kwargs):
    forms = [bootstrap_form(f, **kwargs) for f in formset]
    return force_text(formset.management_form) + '\n' + '\n'.join(forms)


@register.simple_tag
def bootstrap_form(form, inline=False, field_class='', label_class='', horizontal=False):
    html = ''
    errors = []
    fields = []
    for field in form:
        fields.append(bootstrap_field(
            field,
            inline=inline,
            field_class=field_class,
            label_class=label_class,
            horizontal=horizontal,
        ))
        if field.is_hidden and field.errors:
            errors += field.errors
    errors += form.non_field_errors()
    if errors:
        html += '<div class="alert alert-danger">%s</div>\n' % '\n'.join(['<p>%s</p>' % e for e in errors])
    return html + '\n'.join(fields)


@register.simple_tag
def bootstrap_field(field, inline=False, horizontal=False, field_class=None, label_class=None, show_label=True):
    # Hiden input required no special treatment
    if field.is_hidden:
        return force_text(field)

    # Read widgets attributes
    widget_attr_class = getattr(field.field.widget.attrs, 'class', '')
    widget_attr_placeholder = getattr(field.field.widget.attrs, 'placeholder', '')
    widget_attr_title = getattr(field.field.widget.attrs, 'title', '')

    # Class to add to field element
    form_control_class = 'form-control'
    # Convert this widget from HTML list to a wrapped class?
    list_to_class = False
    # Wrap rendered field in its own label?
    put_inside_label = False
    # Wrapper for the final result (should contain %s if not empty)
    wrapper = ''

    # Adjust workings for various widget types
    if isinstance(field.field.widget, widgets.CheckboxInput):
        form_control_class = ''
        put_inside_label = True
        wrapper = '<div class="checkbox">%s</div>'
    elif isinstance(field.field.widget, widgets.RadioSelect):
        form_control_class = ''
        list_to_class = 'radio'
    elif isinstance(field.field.widget, widgets.CheckboxSelectMultiple):
        form_control_class = ''
        list_to_class = 'checkbox'

    # Temporarily adjust to widget class and placeholder attributes if necessary
    if form_control_class:
        field.field.widget.attrs['class'] = add_css_class(widget_attr_class, form_control_class)
    if field.label and not put_inside_label and not widget_attr_placeholder:
        field.field.widget.attrs['placeholder'] = field.label
    if not put_inside_label and not widget_attr_title:
        field.field.widget.attrs['title'] = field.help_text

    # Render the field
    rendered_field = force_text(field)

    # Return class and placeholder attributes to original settings
    field.field.widget.attrs['class'] = widget_attr_class
    field.field.widget.attrs['placeholder'] = widget_attr_placeholder
    field.field.widget.attrs['title'] = widget_attr_title

    # Handle widgets that are rendered as lists
    if list_to_class:
        mapping = [
            ('<ul', '<div'),
            ('</ul>', '</div>'),
            ('<li', '<div class="%s"' % list_to_class),
            ('</li>', '</div>'),
        ]
        for k, v in mapping:
            rendered_field = rendered_field.replace(k, v)

    # Wrap the rendered field in its label if necessary
    if put_inside_label:
        rendered_field = bootstrap_label(rendered_field + ' ' + field.label, label_title=field.help_text)

    # Add any help text and/or errors
    if not inline:
        help_text_and_errors = []
        if field.help_text:
            help_text_and_errors.append((field.help_text))
        if field.errors:
            help_text_and_errors += field.errors
        if help_text_and_errors:
            rendered_field += '<span class="help-block">%s</span>' % ' '.join(help_text_and_errors)

    # Wrap the rendered field
    if wrapper:
        rendered_field = wrapper % rendered_field

    # Wrap the rendered field in a class if set
    if field_class:
        rendered_field = '<div class="%s">%s</div>' % (field_class, rendered_field)

    # Prepare label, horizontal forms require a small trick
    label = field.label
    if put_inside_label:
        label = None
    if inline or not show_label:
        label_class = add_css_class(label_class, 'sr-only')

    # Render label and field
    content = bootstrap_combine_field_and_label(
        field=rendered_field,
        label=label,
        field_class=field_class,
        label_class=label_class,
        horizontal=horizontal,
    )

    # Return combined content, wrapped in form control
    form_group_class = ''
    if field.errors:
        form_group_class = 'has-error'
    elif field.form.is_bound:
        form_group_class = 'has-success'
    return bootstrap_form_group(content, form_group_class)


@register.simple_tag()
def bootstrap_label(content, label_for=None, label_class=None, label_title=''):
    attrs = {}
    if label_for:
        attrs['for'] = label_for
    if label_class:
        attrs['class'] = label_class
    if label_title:
        attrs['title'] = label_title
    return '<label%(attrs)s>%(content)s</label>' % {
        'attrs': flatatt(attrs),
        'content': content,
    }


@register.simple_tag
def bootstrap_form_buttons(**kwargs):
    buttons = []
    submit = kwargs.get('submit', None)
    cancel = kwargs.get('cancel', None)
    if submit:
        buttons.append(bootstrap_button(submit, 'submit'))
    if cancel:
        buttons.append(bootstrap_button(cancel, 'cancel'))
    buttons = ' '.join(buttons)
    kwargs2 = kwargs.copy()
    kwargs2.update({
        'label': None,
        'field': buttons,
    })
    return bootstrap_form_group(bootstrap_combine_field_and_label(**kwargs2))


@register.simple_tag
def bootstrap_button(content, button_type=None):
    attrs = {}
    if button_type:
        attrs['type'] = button_type
    attrs['class'] = 'btn'
    if button_type == 'submit':
        attrs['class'] += ' btn-primary'
    return '<button%(attrs)s>%(content)s</button>' % {
        'attrs': flatatt(attrs),
        'content': content,
    }


def bootstrap_combine_field_and_label(field, label, field_class='', label_class='', horizontal=False, **kwargs):
    # Default settings for horizontal form
    if horizontal:
        if not field_class:
            label_class = 'col-lg-2'
            field_class = 'col-lg-10'
        if not label:
            label = '&nbsp;'
        label_class = add_css_class(label_class, 'control-label')
    html = field
    if field_class:
        html = '<div class="%s">%s</div>' % (field_class, html)
    if label:
        html = bootstrap_label(label, label_class=label_class) + html
    return html


def bootstrap_form_group(content, css_class=''):
    return '<div class="%(class)s">%(content)s</div>' % {
        'class': add_css_class(FORM_GROUP_CLASS, css_class),
        'content': content,
    }

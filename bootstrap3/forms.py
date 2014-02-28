from __future__ import unicode_literals

from django.contrib.admin.widgets import AdminFileWidget
from django.forms import HiddenInput, FileInput, CheckboxSelectMultiple, Textarea, TextInput, RadioSelect, \
    CheckboxInput
from django.forms.forms import BaseForm, BoundField
from django.forms.formsets import BaseFormSet
from django.forms.widgets import flatatt
from django.utils.encoding import force_text
from django.utils.html import conditional_escape, strip_tags

from .bootstrap import get_bootstrap_setting
from .exceptions import BootstrapError
from .html import add_css_class
from .icons import render_icon


FORM_GROUP_CLASS = 'form-group'


def render_formset(formset, **kwargs):
    if not isinstance(formset, BaseFormSet):
        raise BootstrapError('Parameter "formset" should contain a valid Django FormSet.')
    forms = [render_form(f, **kwargs) for f in formset]
    return force_text(formset.management_form) + '\n' + '\n'.join(forms)


def render_form(form, layout='', form_group_class=FORM_GROUP_CLASS,
                field_class='', label_class='', show_help=True, exclude='', set_required=True):
    if not isinstance(form, BaseForm):
        raise BootstrapError('Parameter "form" should contain a valid Django Form.')
    html = ''
    errors = []
    fields = []
    for field in form:
        fields.append(render_field(
            field,
            layout=layout,
            form_group_class=form_group_class,
            field_class=field_class,
            label_class=label_class,
            show_help=show_help,
            exclude=exclude,
            set_required=set_required,
        ))
        if field.is_hidden and field.errors:
            errors += field.errors
    errors += form.non_field_errors()
    if errors:
        html += '''<div class="alert alert-danger alert-dismissable alert-link">
                   <button class=close data-dismiss=alert aria-hidden=true>
                   &times;</button>{errors}</div>\n
                '''.format(errors='\n'.join(['<p>{e}</p>'.format(e=e) for e in errors]))
    return html + '\n'.join(fields)


def render_field(field, layout='', form_group_class=FORM_GROUP_CLASS,
                 field_class=None, label_class=None, show_label=True,
                 show_help=True, exclude='', set_required=True):
    # Only allow BoundField
    if not isinstance(field, BoundField):
        raise BootstrapError('Parameter "field" should contain a valid Django BoundField.')
    # See if we're not excluded
    if field.name in exclude.replace(' ', '').split(','):
        return ''
    # Hidden input requires no special treatment
    if field.is_hidden:
        return force_text(field)
    # Shortcut to widget
    widget = field.field.widget
    # Read widgets attributes
    widget_attrs = {
        'class': widget.attrs.get('class', ''),
        'placeholder': widget.attrs.get('placeholder', ''),
        'title': widget.attrs.get('title', ''),
    }
    # Class to add to field element
    if isinstance(widget, FileInput):
        form_control_class = ''
    else:
        form_control_class = 'form-control'
    # Convert this widget from HTML list to a wrapped class?
    list_to_class = False
    # Wrap rendered field in its own label?
    put_inside_label = False
    # Wrapper for the final result (should contain %s if not empty)
    wrapper = ''
    # Adjust workings for various widget types
    if isinstance(field.field.widget, CheckboxInput):
        form_control_class = ''
        put_inside_label = True
        wrapper = '<div class=checkbox>{content}</div>'
    elif isinstance(widget, RadioSelect):
        form_control_class = ''
        list_to_class = 'radio'
    elif isinstance(widget, CheckboxSelectMultiple):
        form_control_class = ''
        list_to_class = 'checkbox'
    # Get help text
    field_help = force_text(field.help_text) if show_help and field.help_text else ''
    # Get errors
    field_errors = [conditional_escape(force_text(error)) for error in field.errors]
    # Temporarily adjust widget attributes if necessary
    if form_control_class:
        widget.attrs['class'] = add_css_class(widget_attrs['class'], form_control_class)
    if is_widget_with_placeholder(widget) and field.label and not put_inside_label and not widget_attrs['placeholder']:
        widget.attrs['placeholder'] = field.label
    if field_help and not put_inside_label and not widget_attrs['title']:
        widget.attrs['title'] = strip_tags(field_help)
    if layout == 'inline' and field_errors:
        field_title = widget.attrs.get('title', '')
        field_title += ' ' + ' '.join([strip_tags(e) for e in field_errors])
        widget.attrs['title'] = field_title.strip()
    # Set required attribute
    if set_required and is_widget_required_attribute(widget):
        widget.attrs['required'] = 'required'
    # Render the field
    rendered_field = field.as_widget(attrs=widget.attrs)
    # Return changed attributes to original settings
    for attr in widget_attrs:
        widget.attrs[attr] = widget_attrs[attr]
    # Handle widgets that are rendered as lists
    if list_to_class:
        mapping = [
            ('<ul', '<div'),
            ('</ul>', '</div>'),
            ('<li', '<div class="{klass}"'.format(klass=list_to_class)),
            ('</li>', '</div>'),
        ]
        for k, v in mapping:
            rendered_field = rendered_field.replace(k, v)
    # Wrap the rendered field in its label if necessary
    if put_inside_label:
        rendered_field = render_label(
            content='{field} {label}'.format(field=rendered_field, label=field.label),
            label_title=field.help_text
        )
    # Add any help text and/or errors
    if layout != 'inline':
        help_text_and_errors = [field_help] + field_errors
        if help_text_and_errors:
            help_html = ' '.join([h for h in help_text_and_errors if h])
            rendered_field += '<span class=help-block>{help}</span>'.format(help=help_html)
    # Wrap the rendered field
    if wrapper:
        rendered_field = wrapper.format(content=rendered_field)
    # Prepare label
    label = field.label
    if put_inside_label:
        label = None
    if layout == 'inline' or not show_label:
        label_class = add_css_class(label_class, 'sr-only')
    # Render label and field
    content = render_field_and_label(
        field=rendered_field,
        label=label,
        field_class=field_class,
        label_class=label_class,
        layout=layout,
    )
    # Return combined content, wrapped in form control
    if field.errors:
        form_group_class = add_css_class(form_group_class, 'has-error')
    elif field.form.is_bound:
        form_group_class = add_css_class(form_group_class, 'has-success')

    return render_form_group(content, form_group_class)


def render_label(content, label_for=None, label_class=None, label_title=''):
    """
    Render a label with content
    """
    attrs = {}
    if label_for:
        attrs['for'] = label_for
    if label_class:
        attrs['class'] = label_class
    if label_title:
        attrs['title'] = label_title
    return '<label{attrs}>{content}</label>'.format(
        attrs=flatatt(attrs),
        content=content
    )


def render_button(content, button_type=None, icon=None):
    attrs = {'class': 'btn'}
    icon_content = ''
    if button_type:
        if button_type == 'submit':
            attrs['class'] += ' btn-primary'
        elif button_type != 'reset' and button_type != 'button':
            raise BootstrapError('Parameter "button_type" should be "submit", "reset", "button" or empty.')
        attrs['type'] = button_type
    if icon:
        icon_content = render_icon(icon) + ' '
    return '<button{attrs}>{content}</button>'.format(
        attrs=flatatt(attrs),
        content='{icon_content}{content}'.format(icon_content=icon_content, content=content)
    )


def render_field_and_label(field, label, field_class='', label_class='', layout='', **kwargs):
    # Default settings for horizontal form
    if layout == 'horizontal':
        if not label_class:
            label_class = get_bootstrap_setting('horizontal_label_class')
        if not field_class:
            field_class = get_bootstrap_setting('horizontal_field_class')
        if not label:
            label = '&nbsp;'
        label_class = add_css_class(label_class, 'control-label')
    html = field
    if field_class:
        html = '<div class="{klass}">{html}</div>'.format(klass=field_class, html=html)
    if label:
        html = render_label(label, label_class=label_class) + html
    return html


def render_form_group(content, css_class=FORM_GROUP_CLASS):
    return '<div class="{klass}">{content}</div>'.format(
        klass=css_class,
        content=content,
    )


def is_widget_required_attribute(widget):
    if not get_bootstrap_setting('set_required'):
        return False
    if not widget.is_required:
        return False
    if isinstance(widget, (AdminFileWidget, HiddenInput, FileInput, CheckboxSelectMultiple)):
        return False
    return True


def is_widget_with_placeholder(widget):
    """
    Is this a widget that should have a placeholder?
    Only text, search, url, tel, e-mail, password, number have placeholders
    These are all derived form TextInput, except for Textarea
    """
    return isinstance(widget, (TextInput, Textarea))


from __future__ import unicode_literals

from django.contrib.admin.widgets import AdminFileWidget
from django.forms import HiddenInput, FileInput, CheckboxSelectMultiple, Textarea, TextInput, RadioSelect, \
    CheckboxInput, ClearableFileInput, DateInput, Select
from django.forms.extras import SelectDateWidget
from django.forms.forms import BaseForm, BoundField
from django.forms.formsets import BaseFormSet
from django.utils.encoding import force_text
from django.utils.html import conditional_escape, strip_tags

from .bootstrap import get_bootstrap_setting
from .text import text_concat
from .exceptions import BootstrapError
from .html import add_css_class, render_tag
from .icons import render_icon


FORM_GROUP_CLASS = 'form-group'


def render_formset(formset, **kwargs):
    """
    Render a formset to a Bootstrap layout
    """
    if not isinstance(formset, BaseFormSet):
        raise BootstrapError('Parameter "formset" should contain a valid Django FormSet.')
    forms = [render_form(f, **kwargs) for f in formset]
    return force_text(formset.management_form) + '\n' + '\n'.join(forms)


def render_form(form, layout='', form_group_class=FORM_GROUP_CLASS, field_class='', label_class='', show_help=True,
                exclude='', set_required=True):
    """
    Render a formset to a Bootstrap layout
    """
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
                 show_help=True, exclude='', set_required=True,
                 addon_before=None, addon_after=None):
    """
    Render a formset to a Bootstrap layout
    """
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
    # Optional extra rendering
    after_render = None
    # Wrap rendered field in its own label?
    put_inside_label = False
    # Wrapper for the final result (should contain {content} if not empty)
    wrapper = ''

    # Adjust workings for various widget types
    if isinstance(field.field.widget, CheckboxInput):
        form_control_class = ''
        put_inside_label = True
        wrapper = '<div class="checkbox">{content}</div>'
    elif isinstance(widget, RadioSelect):
        form_control_class = ''
        after_render = list_to_class('radio')
    elif isinstance(widget, CheckboxSelectMultiple):
        form_control_class = ''
        after_render = list_to_class('checkbox')
    elif isinstance(widget, SelectDateWidget):
        after_render = fix_date_select_input
    elif isinstance(widget, ClearableFileInput):
        after_render = fix_clearable_file_input

    # Handle addons
    if (addon_before or addon_after) and is_widget_with_addon_support(widget):
        if not wrapper:
            wrapper = '{content}'
        before = '<span class="input-group-addon">{addon}</span>'.format(addon=addon_before) if addon_before else ''
        after = '<span class="input-group-addon">{addon}</span>'.format(addon=addon_after) if addon_after else ''
        content = '<div class="input-group">{before}{content}{after}</div>'.format(
            before=before,
            after=after,
            content='{content}',
        )
        wrapper = wrapper.format(content=content)

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
    # Apply the post_processor
    if after_render:
        rendered_field = after_render(rendered_field)
    # Return changed attributes to original settings
    for attr in widget_attrs:
        widget.attrs[attr] = widget_attrs[attr]
    # Wrap the rendered field in its label if necessary
    if put_inside_label:
        rendered_field = render_label(
            content='{field} {label}'.format(field=rendered_field, label=field.label),
            label_title=field.help_text
        )
    
    # Wrap the rendered field
    if wrapper:
        rendered_field = wrapper.format(content=rendered_field)

    # Add any help text and/or errors
    if layout != 'inline':
        help_text_and_errors = [field_help] + field_errors if field_help else field_errors
        if help_text_and_errors:
            help_html = ' '.join([h for h in help_text_and_errors if h])
            rendered_field += '<span class=help-block>{help}</span>'.format(help=help_html)
    
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

    # Required and optional classes to the form group
    if field.field.required:
        form_group_class = add_css_class(form_group_class, 'required')
    else:
        form_group_class = add_css_class(form_group_class, 'optional')

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
    return render_tag('label', attrs=attrs, content=content)


def render_button(content, button_type=None, icon=None):
    attrs = {'class': 'btn'}
    if button_type:
        if button_type == 'submit':
            attrs['class'] += ' btn-primary'
        elif button_type != 'reset' and button_type != 'button':
            raise BootstrapError('Parameter "button_type" should be "submit", "reset", "button" or empty.')
        attrs['type'] = button_type
    icon_content = render_icon(icon) if icon else ''
    return render_tag('button', attrs=attrs, content=text_concat(icon_content, content, separator=' '))


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
    """
    Render a Bootstrap form group
    """
    return '<div class="{klass}">{content}</div>'.format(
        klass=css_class,
        content=content,
    )


def is_widget_required_attribute(widget):
    """
    Is this widget required?
    """
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


def is_widget_with_addon_support(widget):
    """
    Is this a widget that supports addons?
    """
    return isinstance(widget, (TextInput, DateInput, Select))


def list_to_class(klass):
    def fixer(html):
        mapping = [
            ('<ul', '<div'),
            ('</ul>', '</div>'),
            ('<li', '<div class="{klass}"'.format(klass=klass)),
            ('</li>', '</div>'),
        ]
        for k, v in mapping:
            html = html.replace(k, v)
        return html

    return fixer


def surround_with(html_with_content):
    def wrapper(html):
        return html_with_content.format(content=html)

    return wrapper


def fix_date_select_input(html):
    div1 = '<div class="col-xs-4">'
    div2 = '</div>'
    html = html.replace('<select', div1 + '<select')
    html = html.replace('</select>', '</select>' + div2)
    return '<div class="row bootstrap3-multi-input">' + html + '</div>'


def fix_clearable_file_input(html):
    """
    Fix a clearable file input
    TODO: This needs improvement

    Currently Django returns
    Currently: <a href="dummy.txt">dummy.txt</a> <input id="file4-clear_id" name="file4-clear" type="checkbox" /> <label for="file4-clear_id">Clear</label><br />Change: <input id="id_file4" name="file4" type="file" /><span class=help-block></span></div>

    """
    # TODO This needs improvement
    return '<div class="row bootstrap3-multi-input"><div class="col-xs-12">' + html + '</div></div>'

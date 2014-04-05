# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import (TextInput, DateInput, FileInput, CheckboxInput,
                          ClearableFileInput, Select, RadioSelect, CheckboxSelectMultiple)
from django.forms.extras import SelectDateWidget
from django.forms.forms import BaseForm, BoundField
from django.utils.encoding import force_text
from django.utils.html import conditional_escape, strip_tags
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from .bootstrap import get_bootstrap_setting
from bootstrap3.text import text_value
from .exceptions import BootstrapError
from .html import add_css_class
from .forms import (render_field, render_label, render_form_group,
                    is_widget_with_placeholder, is_widget_required_attribute, FORM_GROUP_CLASS)


class FormRenderer(object):
    """
    Default form renderer
    """

    def __init__(self, form, layout='', form_group_class=FORM_GROUP_CLASS,
                 field_class='', label_class='', show_help=True, exclude='',
                 set_required=True):
        if not isinstance(form, BaseForm):
            raise BootstrapError(
                'Parameter "form" should contain a valid Django Form.')
        self.form = form
        self.layout = layout
        self.form_group_class = form_group_class
        self.field_class = field_class
        self.label_class = label_class
        self.show_help = show_help
        self.exclude = exclude
        self.set_required = set_required

    def render_fields(self):
        rendered_fields = []
        for field in self.form:
            rendered_fields.append(render_field(
                field,
                layout=self.layout,
                form_group_class=self.form_group_class,
                field_class=self.field_class,
                label_class=self.label_class,
                show_help=self.show_help,
                exclude=self.exclude,
                set_required=self.set_required,
            ))
        return '\n'.join(rendered_fields)

    def get_form_errors(self):
        form_errors = []
        for field in self.form:
            if field.is_hidden and field.errors:
                form_errors += field.errors
        return form_errors + self.form.non_field_errors()

    def render_errors(self):
        form_errors = self.get_form_errors()
        if form_errors:
            errors = '\n'.join(['<p>{e}</p>'.format(e=e) for e in form_errors])
            return '''
                <div class="alert alert-danger alert-dismissable alert-link">
                <button class="close" data-dismiss="alert" aria-hidden="true">
                &times;</button>{errors}</div>\n'''.format(errors=errors)
        return ''

    def render(self):
        return self.render_errors() + self.render_fields()


class FieldRenderer(object):
    """
    Default field renderer
    """

    def __init__(self, field, layout='', form_group_class=FORM_GROUP_CLASS,
                 field_class=None, label_class=None, show_label=True,
                 show_help=True, exclude='', set_required=True,
                 addon_before=None, addon_after=None):
        # Only allow BoundField
        if not isinstance(field, BoundField):
            raise BootstrapError('Parameter "field" should contain a valid Django BoundField.')

        self.field = field
        self.layout = layout
        self.form_group_class = form_group_class
        self.field_class = field_class
        self.label_class = label_class
        self.show_label = show_label
        self.exclude = exclude
        self.set_required = set_required
        self.widget = field.field.widget
        self.initial_attrs = self.widget.attrs.copy()
        self.field_help = force_text(mark_safe(field.help_text)) if show_help and field.help_text else ''
        self.field_errors = [conditional_escape(force_text(error)) for error in field.errors]
        self.placeholder = field.label
        self.form_error_class = getattr(field.form, 'error_css_class', '')
        self.form_required_class = getattr(field.form, 'required_css_class', '')
        self.addon_before = addon_before
        self.addon_after = addon_after

    def restore_widget_attrs(self):
        self.widget.attrs = self.initial_attrs

    def add_class_attrs(self):
        self.widget.attrs['class'] = self.widget.attrs.get('class', '')
        if not isinstance(self.widget, (CheckboxInput,
                                        RadioSelect,
                                        CheckboxSelectMultiple,
                                        FileInput)):
            self.widget.attrs['class'] = add_css_class(
                self.widget.attrs['class'], 'form-control')

    def add_placeholder_attrs(self):
        placeholder = self.widget.attrs.get('placeholder', self.placeholder)
        if placeholder and is_widget_with_placeholder(self.widget):
            self.widget.attrs['placeholder'] = placeholder

    def add_help_attrs(self):
        title = self.widget.attrs.get('title', strip_tags(self.field_help))
        if not isinstance(self.widget, CheckboxInput):
            self.widget.attrs['title'] = title

    def add_required_attrs(self):
        if self.set_required and is_widget_required_attribute(self.widget):
            self.widget.attrs['required'] = 'required'

    def add_widget_attrs(self):
        self.add_class_attrs()
        self.add_placeholder_attrs()
        self.add_help_attrs()
        self.add_required_attrs()

    def list_to_class(self, html, klass):
        mapping = [
            ('<ul', '<div'),
            ('</ul>', '</div>'),
            ('<li', '<div class="{klass}"'.format(klass=klass)),
            ('</li>', '</div>'),
        ]
        for k, v in mapping:
            html = html.replace(k, v)
        return html

    def put_inside_label(self, html):
        content = '{field} {label}'.format(field=html, label=self.field.label)
        return render_label(content=content, label_title=strip_tags(self.field_help))

    def fix_date_select_input(self, html):
        div1 = '<div class="col-xs-4">'
        div2 = '</div>'
        html = html.replace('<select', div1 + '<select')
        html = html.replace('</select>', '</select>' + div2)
        return '<div class="row bootstrap3-multi-input">' + html + '</div>'

    def fix_clearable_file_input(self, html):
        """
        Fix a clearable file input
        TODO: This needs improvement

        Currently Django returns
        Currently: <a href="dummy.txt">dummy.txt</a> <input id="file4-clear_id" name="file4-clear" type="checkbox" /> <label for="file4-clear_id">Clear</label><br />Change: <input id="id_file4" name="file4" type="file" /><span class=help-block></span></div>

        """
        # TODO This needs improvement
        return '<div class="row bootstrap3-multi-input"><div class="col-xs-12">' + html + '</div></div>'

    def post_widget_render(self, html):
        if isinstance(self.widget, RadioSelect):
            html = self.list_to_class(html, 'radio')
        elif isinstance(self.widget, CheckboxSelectMultiple):
            html = self.list_to_class(html, 'checkbox')
        elif isinstance(self.widget, SelectDateWidget):
            html = self.fix_date_select_input(html)
        elif isinstance(self.widget, ClearableFileInput):
            html = self.fix_clearable_file_input(html)
        elif isinstance(self.widget, CheckboxInput):
            html = self.put_inside_label(html)
        return html

    def wrap_widget(self, html):
        if isinstance(self.widget, CheckboxInput):
            html = '<div class="checkbox">{content}</div>'.format(content=html)
        return html

    def make_input_group(self, html):
        if ((self.addon_before or self.addon_after) and
                isinstance(self.widget, (TextInput, DateInput, Select))
        ):
            before = '<span class="input-group-addon">{addon}</span>'.format(
                addon=self.addon_before) if self.addon_before else ''
            after = '<span class="input-group-addon">{addon}</span>'.format(
                addon=self.addon_after) if self.addon_after else ''
            html = '<div class="input-group">{before}{html}{after}</div>'.format(
                before=before, after=after, html=html)
        return html

    def append_to_field(self, html):
        help_text_and_errors = [self.field_help] + self.field_errors \
            if self.field_help else self.field_errors
        if help_text_and_errors:
            help_html = get_template(
                'bootstrap3/field_help_text_and_errors.html').render(Context({
                'field': self.field,
                'help_text_and_errors': help_text_and_errors,
                'layout': self.layout,
            }))
            html += '<span class="help-block">{help}</span>'.format(help=help_html)
        return html

    def get_field_class(self):
        field_class = self.field_class
        if not field_class and self.layout == 'horizontal':
            field_class = get_bootstrap_setting('horizontal_field_class')
        return field_class

    def wrap_field(self, html):
        field_class = self.get_field_class()
        if field_class:
            html = '<div class="{klass}">{html}</div>'.format(klass=field_class, html=html)
        return html

    def get_label_class(self):
        label_class = self.label_class
        if not label_class and self.layout == 'horizontal':
            label_class = get_bootstrap_setting('horizontal_label_class')
        label_class = text_value(label_class)
        if not self.show_label:
            label_class = add_css_class(label_class, 'sr-only')
        return add_css_class(label_class, 'control-label')

    def get_label(self):
        if isinstance(self.widget, CheckboxInput):
            label = None
        else:
            label = self.field.label
        if self.layout == 'horizontal' and not label:
            return '&#160;'
        return label

    def add_label(self, html):
        label = self.get_label()
        if label:
            html = render_label(label, label_class=self.get_label_class()) + html
        return html

    def get_form_group_class(self):
        form_group_class = self.form_group_class
        if self.field.errors and self.form_error_class:
            form_group_class = add_css_class(
                form_group_class, self.form_error_class)
        if self.field.field.required and self.form_required_class:
            form_group_class = add_css_class(
                form_group_class, self.form_required_class)
        if self.field_errors:
            form_group_class = add_css_class(form_group_class, 'has-error')
        elif self.field.form.is_bound:
            form_group_class = add_css_class(form_group_class, 'has-success')
        return form_group_class

    def wrap_label_and_field(self, html):
        return render_form_group(html, self.get_form_group_class())

    def render(self):
        # See if we're not excluded
        if self.field.name in self.exclude.replace(' ', '').split(','):
            return ''
        # Hidden input requires no special treatment
        if self.field.is_hidden:
            return force_text(self.field)
        self.add_widget_attrs()
        html = self.field.as_widget(attrs=self.widget.attrs)
        self.restore_widget_attrs()
        html = self.post_widget_render(html)
        html = self.wrap_widget(html)
        html = self.make_input_group(html)
        html = self.append_to_field(html)
        html = self.wrap_field(html)
        html = self.add_label(html)
        html = self.wrap_label_and_field(html)
        return html


class InlineFieldRenderer(FieldRenderer):
    """
    Inline field renderer
    """

    def add_error_attrs(self):
        field_title = self.widget.attrs.get('title', '')
        field_title += ' ' + ' '.join([strip_tags(e) for e in self.field_errors])
        self.widget.attrs['title'] = field_title.strip()

    def add_widget_attrs(self):
        super(InlineFieldRenderer, self).add_widget_attrs()
        self.add_error_attrs()

    def append_to_field(self, html):
        return html

    def get_field_class(self):
        return self.field_class

    def get_label_class(self):
        return add_css_class(self.label_class, 'sr-only')

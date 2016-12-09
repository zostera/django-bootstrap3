# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
from django.forms import (
    TextInput, DateInput, FileInput, CheckboxInput, MultiWidget,
    ClearableFileInput, Select, RadioSelect, CheckboxSelectMultiple
)
from django.forms.extras import SelectDateWidget
from django.forms.forms import BaseForm, BoundField
from django.forms.formsets import BaseFormSet
from django.utils.html import conditional_escape, escape, strip_tags
from django.utils.safestring import mark_safe
from django.template import Context

from .bootstrap import get_bootstrap_setting
from .exceptions import BootstrapError
from .forms import (
    render_form, render_field, render_label, render_form_group,
    is_widget_with_placeholder, is_widget_required_attribute, FORM_GROUP_CLASS
)
from .text import text_value
from .utils import add_css_class, render_template_file


class BaseRenderer(object):
    """
    A content renderer
    """

    def __init__(self, *args, **kwargs):
        self.layout = kwargs.get('layout', '')
        self.form_group_class = kwargs.get(
            'form_group_class', FORM_GROUP_CLASS)
        self.field_class = kwargs.get('field_class', '')
        self.label_class = kwargs.get('label_class', '')
        self.show_help = kwargs.get('show_help', True)
        self.show_label = kwargs.get('show_label', True)
        self.exclude = kwargs.get('exclude', '')
        self.set_required = kwargs.get('set_required', True)
        self.set_disabled = kwargs.get('set_disabled', False)
        self.size = self.parse_size(kwargs.get('size', ''))
        self.horizontal_label_class = kwargs.get(
            'horizontal_label_class',
            get_bootstrap_setting('horizontal_label_class')
        )
        self.horizontal_field_class = kwargs.get(
            'horizontal_field_class',
            get_bootstrap_setting('horizontal_field_class')
        )

    def parse_size(self, size):
        size = text_value(size).lower().strip()
        if size in ('sm', 'small'):
            return 'small'
        if size in ('lg', 'large'):
            return 'large'
        if size in ('md', 'medium', ''):
            return 'medium'
        raise BootstrapError('Invalid value "%s" for parameter "size" (expected "sm", "md", "lg" or "").' % size)

    def get_size_class(self, prefix='input'):
        if self.size == 'small':
            return prefix + '-sm'
        if self.size == 'large':
            return prefix + '-lg'
        return ''

    def _render(self):
        return ''

    def render(self):
        return mark_safe(self._render())


class FormsetRenderer(BaseRenderer):
    """
    Default formset renderer
    """

    def __init__(self, formset, *args, **kwargs):
        if not isinstance(formset, BaseFormSet):
            raise BootstrapError(
                'Parameter "formset" should contain a valid Django Formset.')
        self.formset = formset
        super(FormsetRenderer, self).__init__(*args, **kwargs)

    def render_management_form(self):
        return text_value(self.formset.management_form)

    def render_form(self, form, **kwargs):
        return render_form(form, **kwargs)

    def render_forms(self):
        rendered_forms = []
        for form in self.formset.forms:
            rendered_forms.append(self.render_form(
                form,
                layout=self.layout,
                form_group_class=self.form_group_class,
                field_class=self.field_class,
                label_class=self.label_class,
                show_label=self.show_label,
                show_help=self.show_help,
                exclude=self.exclude,
                set_required=self.set_required,
                set_disabled=self.set_disabled,
                size=self.size,
                horizontal_label_class=self.horizontal_label_class,
                horizontal_field_class=self.horizontal_field_class,
            ))
        return '\n'.join(rendered_forms)

    def get_formset_errors(self):
        return self.formset.non_form_errors()

    def render_errors(self):
        formset_errors = self.get_formset_errors()
        if formset_errors:
            return render_template_file(
                'bootstrap3/form_errors.html',
                context={
                    'errors': formset_errors,
                    'form': self.formset,
                    'layout': self.layout,
                }
            )
        return ''

    def _render(self):
        return ''.join(
            [
                self.render_errors(),
                self.render_management_form(),
                self.render_forms(),
            ]
        )


class FormRenderer(BaseRenderer):
    """
    Default form renderer
    """

    def __init__(self, form, *args, **kwargs):
        if not isinstance(form, BaseForm):
            raise BootstrapError(
                'Parameter "form" should contain a valid Django Form.')
        self.form = form
        super(FormRenderer, self).__init__(*args, **kwargs)
        # Handle form.empty_permitted
        if self.form.empty_permitted:
            self.set_required = False
        self.error_css_class = kwargs.get('error_css_class', None)
        self.required_css_class = kwargs.get('required_css_class', None)
        self.bound_css_class = kwargs.get('bound_css_class', None)

    def render_fields(self):
        rendered_fields = []
        for field in self.form:
            rendered_fields.append(render_field(
                field,
                layout=self.layout,
                form_group_class=self.form_group_class,
                field_class=self.field_class,
                label_class=self.label_class,
                show_label=self.show_label,
                show_help=self.show_help,
                exclude=self.exclude,
                set_required=self.set_required,
                set_disabled=self.set_disabled,
                size=self.size,
                horizontal_label_class=self.horizontal_label_class,
                horizontal_field_class=self.horizontal_field_class,
                error_css_class=self.error_css_class,
                required_css_class=self.required_css_class,
                bound_css_class=self.bound_css_class,
            ))
        return '\n'.join(rendered_fields)

    def get_fields_errors(self):
        form_errors = []
        for field in self.form:
            if field.is_hidden and field.errors:
                form_errors += field.errors
        return form_errors

    def render_errors(self, type='all'):
        form_errors = None
        if type == 'all':
            form_errors = self.get_fields_errors() + self.form.non_field_errors()
        elif type == 'fields':
            form_errors = self.get_fields_errors()
        elif type == 'non_fields':
            form_errors = self.form.non_field_errors()

        if form_errors:
            return render_template_file(
                'bootstrap3/form_errors.html',
                context={
                    'errors': form_errors,
                    'form': self.form,
                    'layout': self.layout,
                }
            )

        return ''

    def _render(self):
        return self.render_errors() + self.render_fields()


class FieldRenderer(BaseRenderer):
    """
    Default field renderer
    """

    # These widgets will not be wrapped in a form-control class
    WIDGETS_NO_FORM_CONTROL = (
        CheckboxInput,
        RadioSelect,
        CheckboxSelectMultiple,
        FileInput,
    )

    def __init__(self, field, *args, **kwargs):
        if not isinstance(field, BoundField):
            raise BootstrapError('Parameter "field" should contain a valid Django BoundField.')
        self.field = field
        super(FieldRenderer, self).__init__(*args, **kwargs)

        self.widget = field.field.widget
        self.is_multi_widget = isinstance(field.field.widget, MultiWidget)
        self.initial_attrs = self.widget.attrs.copy()
        self.field_help = text_value(mark_safe(field.help_text)) if self.show_help and field.help_text else ''
        self.field_errors = [conditional_escape(text_value(error)) for error in field.errors]

        if get_bootstrap_setting('set_placeholder'):
            self.placeholder = field.label
        else:
            self.placeholder = ''

        self.addon_before = kwargs.get('addon_before', self.widget.attrs.pop('addon_before', ''))
        self.addon_after = kwargs.get('addon_after', self.widget.attrs.pop('addon_after', ''))

        # These are set in Django or in the global BOOTSTRAP3 settings, and
        # they can be overwritten in the template
        error_css_class = kwargs.get('error_css_class', None)
        required_css_class = kwargs.get('required_css_class', None)
        bound_css_class = kwargs.get('bound_css_class', None)
        if error_css_class is not None:
            self.error_css_class = error_css_class
        else:
            self.error_css_class = getattr(
                field.form, 'error_css_class',
                get_bootstrap_setting('error_css_class'))
        if required_css_class is not None:
            self.required_css_class = required_css_class
        else:
            self.required_css_class = getattr(
                field.form, 'required_css_class',
                get_bootstrap_setting('required_css_class'))
        if bound_css_class is not None:
            self.success_css_class = bound_css_class
        else:
            self.success_css_class = getattr(
                field.form, 'bound_css_class',
                get_bootstrap_setting('success_css_class'))

        # Handle form.empty_permitted
        if self.field.form.empty_permitted:
            self.set_required = False
            self.required_css_class = ''

        self.set_disabled = kwargs.get('set_disabled', False)

    def restore_widget_attrs(self):
        self.widget.attrs = self.initial_attrs.copy()

    def add_class_attrs(self, widget=None):
        if widget is None:
            widget = self.widget
        classes = widget.attrs.get('class', '')
        if isinstance(widget, ReadOnlyPasswordHashWidget):
            # Render this is a static control
            classes = add_css_class(classes, 'form-control-static', prepend=True)
        elif not isinstance(widget, self.WIDGETS_NO_FORM_CONTROL):
            classes = add_css_class(classes, 'form-control', prepend=True)
            # For these widget types, add the size class here
            classes = add_css_class(classes, self.get_size_class())
        widget.attrs['class'] = classes

    def add_placeholder_attrs(self, widget=None):
        if widget is None:
            widget = self.widget
        placeholder = widget.attrs.get('placeholder', self.placeholder)
        if placeholder and is_widget_with_placeholder(widget):
            # TODO: Should this be stripped and/or escaped?
            widget.attrs['placeholder'] = placeholder

    def add_help_attrs(self, widget=None):
        if widget is None:
            widget = self.widget
        if not isinstance(widget, CheckboxInput):
            widget.attrs['title'] = widget.attrs.get(
                'title',
                escape(strip_tags(self.field_help))
            )

    def add_required_attrs(self, widget=None):
        if widget is None:
            widget = self.widget
        if self.set_required and is_widget_required_attribute(widget):
            widget.attrs['required'] = 'required'

    def add_disabled_attrs(self, widget=None):
        if widget is None:
            widget = self.widget
        if self.set_disabled:
            widget.attrs['disabled'] = 'disabled'

    def add_widget_attrs(self):
        if self.is_multi_widget:
            widgets = self.widget.widgets
        else:
            widgets = [self.widget]
        for widget in widgets:
            self.add_class_attrs(widget)
            self.add_placeholder_attrs(widget)
            self.add_help_attrs(widget)
            self.add_required_attrs(widget)
            self.add_disabled_attrs(widget)

    def list_to_class(self, html, klass):
        classes = add_css_class(klass, self.get_size_class())
        mapping = [
            ('<ul', '<div'),
            ('</ul>', '</div>'),
            ('<li', '<div class="{klass}"'.format(klass=classes)),
            ('</li>', '</div>'),
        ]
        for k, v in mapping:
            html = html.replace(k, v)
        return html

    def put_inside_label(self, html):
        content = '{field} {label}'.format(
            field=html,
            label=self.field.label,
        )
        return render_label(
            content=mark_safe(content),
            label_for=self.field.id_for_label,
            label_title=escape(strip_tags(self.field_help))
        )

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
        Currently:
        <a href="dummy.txt">dummy.txt</a>
        <input id="file4-clear_id" name="file4-clear" type="checkbox" />
        <label for="file4-clear_id">Clear</label><br />
        Change: <input id="id_file4" name="file4" type="file" />
        <span class=help-block></span>
        </div>

        """
        # TODO This needs improvement
        return '<div class="row bootstrap3-multi-input"><div class="col-xs-12">{html}</div></div>'.format(
            html=html
        )

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
            checkbox_class = add_css_class('checkbox', self.get_size_class())
            html = '<div class="{klass}">{content}</div>'.format(
                klass=checkbox_class,
                content=html,
            )
        return html

    def make_input_group(self, html):
        if (self.addon_before or self.addon_after) and isinstance(self.widget, (TextInput, DateInput, Select)):
            before = '<span class="input-group-addon">{addon}</span>'.format(
                addon=self.addon_before) if self.addon_before else ''
            after = '<span class="input-group-addon">{addon}</span>'.format(
                addon=self.addon_after) if self.addon_after else ''
            html = '<div class="input-group">{before}{html}{after}</div>'.format(
                before=before,
                after=after,
                html=html
            )
        return html

    def append_to_field(self, html):
        help_text_and_errors = []
        if self.field_help:
            help_text_and_errors.append(self.field_help)
        help_text_and_errors += self.field_errors
        if help_text_and_errors:
            help_html = render_template_file(
                'bootstrap3/field_help_text_and_errors.html',
                context=Context({
                    'field': self.field,
                    'help_text_and_errors': help_text_and_errors,
                    'layout': self.layout,
                })
            )
            html += '<span class="help-block">{help}</span>'.format(help=help_html)
        return html

    def get_field_class(self):
        field_class = self.field_class
        if not field_class and self.layout == 'horizontal':
            field_class = self.horizontal_field_class
        return field_class

    def wrap_field(self, html):
        field_class = self.get_field_class()
        if field_class:
            html = '<div class="{klass}">{html}</div>'.format(
                klass=field_class, html=html)
        return html

    def get_label_class(self):
        label_class = self.label_class
        if not label_class and self.layout == 'horizontal':
            label_class = self.horizontal_label_class
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
            return mark_safe('&#160;')
        return label

    def add_label(self, html):
        label = self.get_label()
        if label:
            html = render_label(
                label,
                label_for=self.field.id_for_label,
                label_class=self.get_label_class()) + html
        return html

    def get_form_group_class(self):
        form_group_class = self.form_group_class
        if self.field.errors and self.error_css_class:
            form_group_class = add_css_class(
                form_group_class, self.error_css_class)
        if self.field.field.required and self.required_css_class:
            form_group_class = add_css_class(
                form_group_class, self.required_css_class)
        if self.field_errors:
            form_group_class = add_css_class(form_group_class, 'has-error')
        elif self.field.form.is_bound:
            form_group_class = add_css_class(
                form_group_class, self.success_css_class)
        if self.layout == 'horizontal':
            form_group_class = add_css_class(
                form_group_class, self.get_size_class(prefix='form-group'))
        return form_group_class

    def wrap_label_and_field(self, html):
        return render_form_group(html, self.get_form_group_class())

    def _render(self):
        # See if we're not excluded
        if self.field.name in self.exclude.replace(' ', '').split(','):
            return ''
        # Hidden input requires no special treatment
        if self.field.is_hidden:
            return text_value(self.field)
        # Render the widget
        self.add_widget_attrs()
        html = self.field.as_widget(attrs=self.widget.attrs)
        self.restore_widget_attrs()
        # Start post render
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
        field_title += ' ' + ' '.join(
            [strip_tags(e) for e in self.field_errors])
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

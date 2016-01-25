#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
module that contains all Layout class used for making a advanced
layout for the forms.

to use this advanced feature, you must use the LayoutFormRenderer
in your settings.py :

    BOOTSTRAP3 = {
        'form_renderers': {
            'default': 'bootstrap3.layout.LayoutFormRenderer',
            }
    }


"""

from __future__ import unicode_literals, print_function, absolute_import, division
import logging

import itertools
from django.forms.forms import Form
from django.utils.safestring import mark_safe

from bootstrap3.exceptions import BootstrapException
from bootstrap3.forms import render_field
from bootstrap3.renderers import FormRenderer
from bootstrap3.utils import render_tag

logger = logging.getLogger(__name__)
__author__ = 'Darius BERNARD'

# compatibility for type str
# found in http://www.rfk.id.au/blog/entry/preparing-pyenchant-for-python-3/
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring


class LayoutFormRenderer(FormRenderer):
    """
    this Renderer use the `fields_layout` attrubute of the form to
    create a advanced layout of the form itself.

    at first, it will compile the content of `fields_layout` into a
    class based Layout. and then, it will delegate to the Layout class the
    rendering of the field itself.
    """
    def render_field(self, field):
        """
        helper used to render a field.
        :parama django.forms.fields.Field field: the field to render
        :return: the html output of the given field
        """
        return render_field(
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
        )

    def create_default_layout(self):
        """
        create a layout from the form. it will give exactly the same layout as
        the base FormRenderer
        :param form:
        :return:
        """
        return Layout(*list(self.form.fields.keys()))

    def get_layout(self):
        """
        return a layout for the given form. will try many way to have one :
        - return the result of `get_layout` if for has this method
        - return the value of fields_layout if form has one
        - create a default layout using `self.create_default_layout`
        :param Form form: the form
        """
        form = self.form
        if hasattr(form, "get_layout"):
            layout = form.get_layout()
        elif hasattr(form, "fields_layout"):
            layout = form.fields_layout
        else:
            layout = self.create_default_layout()
        if not isinstance(layout, Layout):
            layout = Layout.from_base_type(layout)
        return layout

    def render_fields(self):
        """
        create the layout and use it to render the form
        :return: the rendered form in html
        :rtype: unicode
        """

        layout = self.get_layout()
        return layout.render(self.form, self)

class LayoutElement(object):
    """
    this class represent a object meant to be used to render a
    special layout into bootstrap3 structure.

    it has 2 jobs : 

    - render the fields into the layout (self.render)
    - transform the base structure into a real layout (self.get_natural_child)

    # rendering

    the rendering of a LayoutElement is done via 3 methods :

    - render(form, renderer)
    - _render(form, renderer)
    - render_children(form, renderer)

    # Layout initalisation

    for readability purpose, the layout writen in the form can be made with
    base class (unicode, list, tuple, dict). it will be compiled into LayoutElement
    class hierarchie which will at render time make the html layout.

    the compilation of the layout from base is done by 3 functions.

    - get_natural_children(children, children_cfg)
    - get_natural_child(attr, cfg)
    - from_base_type(base_value, cfg)

    ## from_base_type

    at first, a subclass of LayoutElement is capable to instantiate itself (via from_base_type) with
    a base type (list/unicode/tuple/dict). it is the job of `from_base_type` to take a data in a base type
    and check if it is usable to instantiate itself.

    ie : a FieldContainer know what to do with a unicode, it will instantiate itself with filename=attr
    ie2 : a Layout don't know what to do with unicode, it will raise TypeError

    ## get_natural_child

    all subclass of LayoutElement must know what to do if their child is not a LayoutElement but a base type.
    for exemple, a Row created with a list, it mean that the row should have many Col. the natural child of a
    Row should be a Col if it was a list.

    this function use the list `natural_child_classes` to make a correspodance between given base type and
    LayoutElement.


    """
    natural_child_classes = [ # type: list[(type, type(LayoutElement))]
        #(unicode, FieldContainer),
        #(list, Row),
        #(tupel, Row),
    ]
    """
    this list of tuple contains the correspances for base type (list/tuples/dict/unicode) into
    the layout natural classes.
    ie : a unicode is meant to be a field in many cases, but an list/tuple depend of the parent.
    """

    def __init__(self, *children, **children_cfg):
        """
        just initialize the current layout with its empty children
        """
        self._children = [] # to make sur that we won't have problème if a repr() is called in next line
        self._children = self.get_natural_children(children, children_cfg) # type: list[LayoutElement]
        """
        the children of the current element. it should be others LayoutElement
        """
        self.layout = None # type: Layout
        """
        the backward link to the current layout
        """

    def add_child(self, child):
        """
        add a child to the current element.
        :param child: an element which will be added.
        :return: the added child in its final form : LayoutElement
        :rtype: LayoutElement
        """
        if isinstance(child, LayoutElement):
            # we just add a already created LayoutElement
            layout_child = child
        else:
            # child can be anything (str, col, etc)
            layout_child = self.get_natural_child(child)
        self._children.append(layout_child)
        return layout_child


    def get_natural_children(self, children, children_cfg):
        """
        take all children given to the construcor and use it to
        create the children list.
        can be overriden create a list of children more aware of the others
        children given.
        :param list children: the list of children given
        :param dict children_cfg: the list of children with theire config given as keyword argument to the constructor
        :return: the list of LayoutElement this Element will have
        :rtype: list[LayoutElement]
        """
        result = []
        for child in children:
            if isinstance(child, LayoutElement):
                # we just add a already created LayoutElement
                layout_child = child
            else:
                # child can be anything (str, col, etc)
                layout_child = self.get_natural_child(child)
            result.append(layout_child)
        for child, cfg in children_cfg.items():
            if isinstance(child, LayoutElement):
                raise TypeError("you cannont give a LayoutElement in the keyword of %s" % self.__class__.__name__)
            else:
                # child can be anything (str, col, etc)
                layout_child = self.get_natural_child(child, cfg)
            result.append(layout_child)
        return result

    @classmethod
    def from_base_type(cls, base_value, cfg=None):
        """
        this method should take a non natural layout value (Row, Col, ...) but a
        base type value (list, unicode, dict) and create the current type with it.

        ie : «ok, I am a Row, and you give me a tuple» => «I must create a Row with as many Col as elements in
        this tuple»

        :param Any base_value: the non layout natural type
        :param cfg: the extra cfg possibly passed to us. ie : Row(field_a="col-md-6")
        :return:  the final Layout natural type
        :rtype: LayoutElement
        """
        raise NotImplementedError()

    def get_natural_child(self, attr, cfg=None):
        """
        AI is there. this method is charged to create the moste intuitive
        layout if the given layout was not made with LayoutElement.

        this method permit to get :

            layout = [
                ("a", "b"),
                "c"
            ]

        and then create the final Layout :

            layout = Layout(
                Row(Col(FieldContainer("a")), Col(FieldContainer("ba")),
                FieldContainer("c")
            )

        if a Row get a child with "a" => it will create a Col("a")
        if the Col get a child with "a" => it will create a FieldContainer("a")
        if the FieldContainer get a "a" => it will be ok !!

        :param attr: the attrubute that is given as a child (it can't be a LayoutElement)
        :param cfg: the extra cfg possibly passed to us. ie : Row(field_a="col-md-6")
        :return:  the corresponding LayouElement
        """
        if isinstance(attr, LayoutElement):
            return attr
        fallback = None
        # for each way to make a child
        for type_from, type_to in self.natural_child_classes:
            if type_from is None:
                fallback = type_to
            else:
                if issubclass(type(attr), type_from):
                    # we transform our «base type» into a LayoutElement
                    return type_to.from_base_type(attr, cfg)

        # if the list contained the value for None, it is
        # meant to be a default type to use as a fallback
        if fallback is not None:
            return fallback.from_base_type(attr, cfg)
        raise BootstrapException("the base type %s cannot be used by %s to make a layout" % (type(attr), self))

    def is_empty(self, form):
        """
        method used to skip rendering a layout part of the form if it don't
        contains anithing.
        :param django.forms.forms.Form form: the current form
        :return: True if the current element is empty (or its children are all empty)
        :rtype: bool
        """
        return len(self._children) == 0 or all((child.is_empty(form) for child in self._children))


    def _render(self, form, renderer):
        """
        render the current element for the form
        :param BaseForm form: the form which is to be rendered
        :param LayoutFormRenderer renderer: the form renderer used to render the current form
        :return: the html output
        :rtype: unicode
        """
        raise NotImplementedError()

    def render(self, form, renderer):
        """
        render the current element if it is not empty
        :param BaseForm form: the form which is to be rendered
        :param LayoutFormRenderer renderer: the form renderer used to render the current form
        :return: the html output
        :rtype: unicode
        """
        if not self.is_empty(form):
            return mark_safe(self._render(form, renderer))
        return ''

    def _render_children(self, form, renderer):
        """
        render all the children without adding anithing
        :param BaseForm form: the form which is to be rendered
        :param LayoutFormRenderer renderer: the form renderer used to render the current form
        :return: the html output
        :rtype: unicode
        """
        return mark_safe("\n".join((child.render(form, renderer) for child in self._children)))

    @classmethod
    def raise_type_error(cls, value, *types):
        """
        helper to raise a consistent message in case of a bad type given to create the layout
        :param Any value: the value given. invalid for this class
        :param type types: the type accepted
        :raise: TypeError
        """
        raise TypeError("%s is not a valid value to create a %s. accepted type is : %s" % (
            value, cls.__name__, ", ".join((t.__name__ for t in types))
        ))

    def _hook_added_to_layout(self, layout):
        """
        hook triggered where a LayoutElement is added in a Layout.
        usefull whene a LayoutElement must be uniq in the layout.
        :param Layout layout:  the layout in which one this Element is Added
        :return: None
        """
        self.layout = layout


    def get_children_fields(self):
        """
        return the field of the current element throuth its children
        :return: the current field
        :rtype: list[unicode]
        """
        return itertools.chain(*(child.get_children_fields() for child in self._children))

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, ", ".join((repr(child) for child in self._children)))

class FieldContainer(LayoutElement):
    """
    Layout element in charge to render the field itself. do not add anything else
    """
    def __init__(self, fieldname):
        """
        :param unicode fieldname: the fieldname of the current form
        :return:
        """
        self.fieldname = fieldname
        super(FieldContainer, self).__init__() # never give it a child. it don't make sens

    def is_empty(self, form):
        """
        check if the form contains the current fieldname
        :return:
        """
        return self.fieldname not in form.fields

    def _render(self, form, renderer):
        """
        render the current field if it exists on the form.
        """
        return renderer.render_field(form[self.fieldname])

    @classmethod
    def from_base_type(cls, base_value, cfg=None):
        if isinstance(base_value, basestring):
            return cls(base_value)
        cls.raise_type_error(base_value, unicode)

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, str(self.fieldname))

    def get_children_fields(self):
        """
        return the field of the current FieldContainer
        :return: the current field
        :rtype: list[unicode]
        """
        return [self.fieldname]



class Col(LayoutElement):
    """
    a column representation in the layout. it represent some <div class="col-md-x"> in the final form.
    it must be contained in the
    """
    # must be a property for cycle usage probleme
    @property
    def natural_child_classes(self):
        return [(basestring, FieldContainer),
            (list, Row),
            (tuple, Row),
            (Ellipsis, EllipsisFieldContainer),
            # todo: manage dict
            #(dict, Fieldset ?)
        ]
    def __init__(self, *children, **children_cfg):
        """
        :param int size: the size of this column in the responsive layout. None mean that it can be updated by the parent row
        :param LayoutElement children: the children that will be inserted in the Cal.
        """
        self.size = children_cfg.pop("size", None)
        super(Col, self).__init__(*children, **children_cfg)


    def render(self, form, renderer):
        """
        render the current element EVEN if it is empty. since cols alocate some space in the layout,
        it must be present to make sure that the next cols won't be moved if self. is empty.
        :param BaseForm form: the form which is to be rendered
        :param LayoutFormRenderer renderer: the form renderer used to render the current form
        :return: the html output
        :rtype: unicode
        """
        return mark_safe(self._render(form, renderer))


    def _render(self, form, renderer):
        """
        render the current field if it exists on the form.
        """

        class_ = "%s-%s" % (renderer.get_size_class("col-") or "col-md" ,self.size or 12)
        return render_tag(
            'div',
            attrs={
                "class": class_
            },
            content=self._render_children(form, renderer)
        )

    @classmethod
    def from_base_type(cls, base_value, cfg=None):
        if cfg is not None:
            # by default, if cfg is a string, it is meant to be the size
            if isinstance(cfg, (basestring, int)):
                size_if_given = {"size": int(cfg)}
            else:
                size_if_given = cfg
        else:
            size_if_given = {}
        if isinstance(base_value, (basestring)):
            return cls(base_value, **size_if_given) # only one child, which is a string
        if isinstance(base_value, (list, tuple)):
            return cls(*base_value, **size_if_given) # as many children as base_value contains
        cls.raise_type_error(base_value, unicode, list, tuple)


class Row(LayoutElement):
    """
    a bootstrap Row that contains many Col
    """

    # must be a property for cycle usage probleme
    @property
    def natural_child_classes(self):
        return [
            (basestring, Col), # Col(basestring) => Col(FieldContainer(basestring))
            (list, Col),
            (tuple, Col),
        ]

    def get_natural_children(self, children, children_cfg):
        """
        we create the Col but we compute the «size» of each that don't already have on to
        make sur that all space will be used
        :return: the size-computed cols
        :rtype: list[LayoutElement]
        """
        result = super(Row, self).get_natural_children(children, children_cfg) # type: list[Col]
        col_that_matters = [
            col for col in result
            if hasattr(col, "size")
        ]
        # we now have a list of Col, but we must compute the size for each that have non given
        unsized = [col for col in col_that_matters if col.size is None]
        available = 12 - sum((col.size for col in col_that_matters if col.size is not None)) or 0
        # now we try to make us of each space left
        while unsized:
            restant = len(unsized)
            col = unsized.pop(0)
            choosed = available // restant
            if choosed <= 0:
                # no more space
                choosed = 1
                # we put a minimun space of 1.
                # the bootstrapException will be raised after the while and it will give more info than we could now
            if available % restant != 0:
                # we will have some space left, we distribute them 1 by 1 to the first cols
                choosed += 1
            col.size = choosed
            available -= choosed
        if available < 0:
            raise BootstrapException("the layout for %r take too many columns. it will take %s/12" % (result, 12 - available))
        return result

    def _render(self, form, renderer):
        """
        render the current field if it exists on the form.
        """
        return render_tag(
            'div',
            attrs={
                "class": "row"
            },
            content=self._render_children(form, renderer)
        )

    @classmethod
    def from_base_type(cls, base_value, cfg=None):
        if isinstance(base_value, (basestring)):
            return cls(base_value) # only one child, which is a string
        if isinstance(base_value, (list, tuple)):
            return cls(*base_value) # as many children as base_value contains
        cls.raise_type_error(base_value, unicode, list, tuple)

    def add_child(self, child):
        raise BootstrapException("impossible to add a element to a Row after its creation.")


class EllipsisFieldContainer(LayoutElement):
    """
    represent a fieldcontainer that will render all missing field in the layout
    it must be uniq in the layout
    """
    field_container_class = FieldContainer
    def __init__(self):
        super(EllipsisFieldContainer, self).__init__()

    def is_empty(self, form):
        if self.layout is None:
            return True
        return len(self.layout.get_missings_fields(form)) == 0

    def _render(self, form, renderer):
        return "\n".join((
            self.field_container_class(f_name).render(form, renderer)
            for f_name in self.layout.get_missings_fields(form)
        ))

    def _hook_added_to_layout(self, layout):
        super(EllipsisFieldContainer, self)._hook_added_to_layout(layout)
        if "EllipsisFieldContainer" in layout.context:
            raise BootstrapException(
                "the layout %r already contain a EllipsisFieldContainer. it must be uniq per Layout" % (layout)
            )
        layout.context["EllipsisFieldContainer"] = self


class Layout(LayoutElement):
    """
    represent a Full layout. it will contains all rows and cols.'
    this is the root structur of a Layout, and add a global context to all its LayoutElement.
    it will add automaticaly the EllipsisFieldContainer if none is manualy added

    >>> Layout.from_base_type([
    ...    "a",
    ...    ("b", "c"),
    ... ])
    Layout(FieldContainer("a"), Row(Col(FieldContainer("b")), Col(FieldContainer("c"))))

    """

    natural_child_classes = [
        (basestring, FieldContainer),
        (list, Row),
        (tuple, Row),
        (Ellipsis, EllipsisFieldContainer),
    ]

    def __init__(self, *args, **kwargs):
        self.context = {}
        self.Ellipsis_field_container = None
        """
        dict that allow sub-LayoutElement to make
        some global Layout variable
        """
        super(Layout, self).__init__(*args, **kwargs)
        for child in self._children:
            child._hook_added_to_layout(self)
        # at this point, all the layout will be provided. so we can add
        # the EllipsisFieldContainer in it if non exists
        if "EllipsisFieldContainer" not in self.context:
            self.add_child(EllipsisFieldContainer())

    def get_missings_fields(self, form):
        """
        list all field in the form that is not listed
        in the current layout
        :param form: the form meant to be displayed
        :rtype: list[unicode]
        :return: the list of fields names
        """
        fields = list(form.fields.keys())
        for layout_field in self.get_children_fields():
            try:
                fields.remove(layout_field)
            except IndexError:
                pass
        return fields

    def add_child(self, child):
        layout_child = super(Layout, self).add_child(child)
        layout_child._hook_added_to_layout(self)


    def _render(self, form, renderer):
        return self._render_children(form, renderer)

    @classmethod
    def from_base_type(cls, base_value, cfg=None):
        if isinstance(base_value, (list, tuple)):
            return cls(*base_value)
        cls.raise_type_error(base_value, list, tuple)

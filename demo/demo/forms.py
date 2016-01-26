# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory

from bootstrap3.layout import Row, Col, FieldContainer
from bootstrap3.tests import TestForm, WellLayoutElement

RADIO_CHOICES = (
    ('1', 'Radio 1'),
    ('2', 'Radio 2'),
)

MEDIA_CHOICES = (
    ('Audio', (
        ('vinyl', 'Vinyl'),
        ('cd', 'CD'),
    )
    ),
    ('Video', (
        ('vhs', 'VHS Tape'),
        ('dvd', 'DVD'),
    )
    ),
    ('unknown', 'Unknown'),
)


class ContactForm(TestForm):
    pass

class LayoutContactForm(TestForm):
    """
    a form with a beautiful layout
    """
    fields_layout = [
        # row with equivalent size col. the absent field will have his space reserved
        ("date", "dontexists", "datetime"),

        # nested row and col
        (
            ("password", "sender"),
            ("message",),
        ),
        # row with equial size, but one is hidden. his space will be reserved
        ("cc_myself", "secret", "select1", "select2"),

        # mixed base and native types
        Row("select3", Col("select4", size=8)),

        # no row nor col. just the field as by default
        "category1",

        # size given in a keyword fashion
        # NOTE : the order of the keywords can't be keept
        #        it will will be rendered with random order
        Row(category2=2, category3=4, category4=4),

        # full native layout
        Row(Col(FieldContainer("addon")), size=4),

        # added a custom LayoutElement `WellLayoutElement` wich contains Ellipsis. this mean
        # that all non given field in the layout will be rendered in a well
        # only in python 3 :
        #WellLayoutElement(...)
        # compatible with both python 2 and 3:
        WellLayoutElement(Ellipsis)
    ]


class ContactBaseFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(ContactBaseFormSet, self).add_fields(form, index)

    def clean(self):
        super(ContactBaseFormSet, self).clean()
        raise forms.ValidationError("This error was added to show the non form errors styling")

ContactFormSet = formset_factory(TestForm, formset=ContactBaseFormSet,
                                 extra=2,
                                 max_num=4,
                                 validate_max=True)


class FilesForm(forms.Form):
    text1 = forms.CharField()
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(widget=forms.ClearableFileInput)
    file5 = forms.ImageField()
    file4 = forms.FileField(required=False, widget=forms.ClearableFileInput)


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data

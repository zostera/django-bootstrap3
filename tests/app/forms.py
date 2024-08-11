from html.parser import HTMLParser

from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.template import engines

RADIO_CHOICES = (("1", "Radio 1"), ("2", "Radio 2"))

MEDIA_CHOICES = (
    ("Audio", (("vinyl", "Vinyl"), ("cd", "CD"))),
    ("Video", (("vhs", "VHS Tape"), ("dvd", "DVD"))),
    ("unknown", "Unknown"),
)


class RadioSetTestForm(forms.Form):
    radio = forms.ChoiceField(widget=forms.RadioSelect, choices=RADIO_CHOICES)


class SmallTestForm(forms.Form):
    sender = forms.EmailField(label="Sender © unicode", help_text='E.g., "me@example.com"')
    subject = forms.CharField(
        max_length=100,
        help_text="my_help_text",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "placeholdertest"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data


class TestForm(forms.Form):
    """Form with a variety of widgets to test bootstrap3 rendering."""

    date = forms.DateField(required=False)
    datetime = forms.SplitDateTimeField(widget=AdminSplitDateTime(), required=False)
    subject = forms.CharField(
        max_length=100,
        help_text="my_help_text",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "placeholdertest"}),
    )
    password = forms.CharField(widget=forms.PasswordInput)
    message = forms.CharField(required=False, help_text="<i>my_help_text</i>")
    sender = forms.EmailField(label="Sender © unicode", help_text='E.g., "me@example.com"')
    secret = forms.CharField(initial=42, widget=forms.HiddenInput)
    weird = forms.CharField(help_text="strings are now utf-8 \u03bcnico\u0394é!")
    cc_myself = forms.BooleanField(
        required=False, help_text='cc stands for "carbon copy." You will get a copy in your mailbox.'
    )
    select1 = forms.ChoiceField(choices=RADIO_CHOICES)
    select2 = forms.MultipleChoiceField(choices=RADIO_CHOICES, help_text="Check as many as you like.")
    select3 = forms.ChoiceField(choices=MEDIA_CHOICES)
    select4 = forms.MultipleChoiceField(choices=MEDIA_CHOICES, help_text="Check as many as you like.")
    category1 = forms.ChoiceField(choices=RADIO_CHOICES, widget=forms.RadioSelect)
    category2 = forms.MultipleChoiceField(
        choices=RADIO_CHOICES, widget=forms.CheckboxSelectMultiple, help_text="Check as many as you like."
    )
    category3 = forms.ChoiceField(widget=forms.RadioSelect, choices=MEDIA_CHOICES)
    category4 = forms.MultipleChoiceField(
        choices=MEDIA_CHOICES, widget=forms.CheckboxSelectMultiple, help_text="Check as many as you like."
    )
    number = forms.FloatField()
    url = forms.URLField()
    addon = forms.CharField(widget=forms.TextInput(attrs={"addon_before": "before", "addon_after": "after"}))

    # TODO: Re-enable this after Django 1.11 #28105 is available
    # polygon = gisforms.PointField()

    required_css_class = "bootstrap3-req"

    # Set this to allow tests to work properly in Django 1.10+
    # More information, see issue #337
    use_required_attribute = False

    def clean(self):
        cleaned_data = super().clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data


class TestFormWithoutRequiredClass(TestForm):
    required_css_class = ""


def render_template(text, context=None):
    """Create a template ``text``."""
    template = engines["django"].from_string(text)
    if not context:
        context = {}
    return template.render(context)


def render_template_with_bootstrap(text, context=None):
    """Create a template ``text`` that first loads bootstrap3."""
    if not context:
        context = {}
    return render_template("{% load bootstrap3 %}" + text, context)


def render_template_with_form(text, context=None):
    """Create a template ``text`` that first loads bootstrap3."""
    if not context:
        context = {}
    if "form" not in context:
        context["form"] = TestForm()
    return render_template_with_bootstrap(text, context)


def render_formset(formset=None, context=None):
    """Create a template that renders a formset."""
    if not context:
        context = {}
    context["formset"] = formset
    return render_template_with_form("{% bootstrap_formset formset %}", context)


def render_form(form=None, context=None):
    """Create a template that renders a form."""
    if not context:
        context = {}
    if form:
        context["form"] = form
    return render_template_with_form("{% bootstrap_form form %}", context)


def render_form_field(field, context=None):
    """Create a template that renders a field."""
    form_field = f"form.{field}"
    return render_template_with_form("{% bootstrap_field " + form_field + " %}", context)


def render_field(field, context=None):
    """Create a template that renders a field."""
    if not context:
        context = {}
    context["field"] = field
    return render_template_with_form("{% bootstrap_field field %}", context)


def get_title_from_html(html):
    class GetTitleParser(HTMLParser):
        def __init__(self):
            try:
                HTMLParser.__init__(self, convert_charrefs=True)
            except TypeError:
                HTMLParser.__init__(self)  # techdebt py27
            self.title = None

        def handle_starttag(self, tag, attrs):
            for attr, value in attrs:
                if attr == "title":
                    self.title = value

    parser = GetTitleParser()
    parser.feed(html)

    return parser.title

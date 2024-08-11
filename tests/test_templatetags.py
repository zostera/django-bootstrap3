import re

from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS
from django.forms import formset_factory
from django.test import TestCase

from bootstrap3.exceptions import BootstrapError
from bootstrap3.text import text_concat, text_value
from bootstrap3.utils import (
    IS_DJANGO5,
    add_css_class,
    render_tag,
    url_to_attrs_dict,
)
from tests.app.forms import (
    RadioSetTestForm,
    SmallTestForm,
    TestForm,
    get_title_from_html,
    render_field,
    render_form,
    render_form_field,
    render_formset,
    render_template_with_form,
)


class FormSetTest(TestCase):
    def test_illegal_formset(self):
        with self.assertRaises(BootstrapError):
            render_formset(formset="illegal")


class FormTest(TestCase):
    def test_illegal_form(self):
        with self.assertRaises(BootstrapError):
            render_form(form="illegal")

    def test_field_names(self):
        form = TestForm()
        res = render_form(form)
        for field in form:
            # datetime has a multiwidget field widget
            if field.name == "datetime":
                self.assertIn('name="datetime_0"', res)
                self.assertIn('name="datetime_1"', res)
            else:
                self.assertIn(f'name="{field.name}"', res)

    def test_field_addons(self):
        form = TestForm()
        res = render_form(form)
        self.assertIn(
            '<div class="input-group"><span class="input-group-addon">before</span><input',
            res,
        )
        self.assertIn('><span class="input-group-addon">after</span></div>', res)

    def test_exclude(self):
        form = TestForm()
        res = render_template_with_form('{% bootstrap_form form exclude="cc_myself" %}', {"form": form})
        self.assertNotIn("cc_myself", res)

    def test_layout_horizontal(self):
        form = TestForm()
        res = render_template_with_form('{% bootstrap_form form layout="horizontal" %}', {"form": form})
        self.assertIn("col-md-3", res)
        self.assertIn("col-md-9", res)
        res = render_template_with_form(
            '{% bootstrap_form form layout="horizontal" '
            + 'horizontal_label_class="hlabel" '
            + 'horizontal_field_class="hfield" %}',
            {"form": form},
        )
        self.assertIn("hlabel", res)
        self.assertIn("hfield", res)

    def test_buttons_tag(self):
        form = TestForm()
        res = render_template_with_form('{% buttons layout="horizontal" %}{% endbuttons %}', {"form": form})
        self.assertIn("col-md-3", res)
        self.assertIn("col-md-9", res)

    def test_error_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap3-err", res)

        res = render_template_with_form(
            '{% bootstrap_form form error_css_class="successful-test" %}',
            {"form": form},
        )
        self.assertIn("successful-test", res)

        res = render_template_with_form('{% bootstrap_form form error_css_class="" %}', {"form": form})
        self.assertNotIn("bootstrap3-err", res)

    def test_required_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap3-req", res)

        res = render_template_with_form(
            '{% bootstrap_form form required_css_class="successful-test" %}',
            {"form": form},
        )
        self.assertIn("successful-test", res)

        res = render_template_with_form('{% bootstrap_form form required_css_class="" %}', {"form": form})
        self.assertNotIn("bootstrap3-req", res)

    def test_bound_class(self):
        form = TestForm({"sender": "sender"})

        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap3-bound", res)

        res = render_template_with_form(
            '{% bootstrap_form form bound_css_class="successful-test" %}',
            {"form": form},
        )
        self.assertIn("successful-test", res)

        res = render_template_with_form('{% bootstrap_form form bound_css_class="" %}', {"form": form})
        self.assertNotIn("bootstrap3-bound", res)

    def test_error_types(self):
        form = SmallTestForm({"sender": "sender"})

        pattern = re.compile(r"\s")

        res = render_template_with_form('{% bootstrap_form form error_types="all" %}', {"form": form})
        expected = """
            <div class="alert alert-danger alert-dismissable alert-link">
               <button class="close" type="button" data-dismiss="alert" aria-hidden="true">&#215;</button>
               Enter a valid email address.<br>
               This field is required.<br>
               This error was added to show the non field errors styling.
           </div>
        """
        self.assertIn(re.sub(pattern, "", expected), re.sub(pattern, "", res))

        res = render_template_with_form('{% bootstrap_form form error_types="non_field_errors" %}', {"form": form})
        expected = """
            <div class="alert alert-danger alert-dismissable alert-link">
                <button class="close" type="button" data-dismiss="alert" aria-hidden="true">&#215;</button>
                This error was added to show the non field errors styling.
            </div>
     """
        self.assertIn(re.sub(pattern, "", expected), re.sub(pattern, "", res))
        res2 = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertEqual(res, res2)

        res = render_template_with_form('{% bootstrap_form form error_types="field_errors" %}', {"form": form})
        expected = """
         <div class="alert alert-danger alert-dismissable alert-link">
            <button class="close" type="button" data-dismiss="alert" aria-hidden="true">&#215;</button>
            Enter a valid email address.<br>
            This field is required.
        </div>
     """
        self.assertIn(re.sub(pattern, "", expected), re.sub(pattern, "", res))


class FieldTest(TestCase):
    def test_illegal_field(self):
        with self.assertRaises(BootstrapError):
            render_field(field="illegal")

    def test_checkbox(self):
        res = render_form_field("cc_myself")
        if IS_DJANGO5:
            res = res.replace('aria-describedby="id_cc_myself_helptext"', "")
        self.assertHTMLEqual(
            """
<div class="form-group">
    <div class="checkbox">
        <label for="id_cc_myself" title="cc stands for &quot;carbon copy.&quot; You will get a copy in your mailbox.">
        <input type="checkbox" name="cc_myself" class="" id="id_cc_myself"> Cc myself
        </label>
    </div>
    <div class="help-block">cc stands for "carbon copy." You will get a copy in your mailbox.</div>
</div>
        """,
            res,
        )

    def test_show_help(self):
        res = render_form_field("subject")
        self.assertIn("my_help_text", res)
        self.assertNotIn("<i>my_help_text</i>", res)
        res = render_template_with_form("{% bootstrap_field form.subject show_help=0 %}")
        self.assertNotIn("my_help_text", res)

    def test_help_with_quotes(self):
        # Checkboxes get special handling, so test a checkbox and something else
        res = render_form_field("sender")
        self.assertEqual(get_title_from_html(res), TestForm.base_fields["sender"].help_text)
        res = render_form_field("cc_myself")
        self.assertEqual(get_title_from_html(res), TestForm.base_fields["cc_myself"].help_text)

    def test_subject(self):
        res = render_form_field("subject")
        self.assertIn('type="text"', res)
        self.assertIn('placeholder="placeholdertest"', res)

    def test_password(self):
        res = render_form_field("password")
        self.assertIn('type="password"', res)
        self.assertIn('placeholder="Password"', res)

    def test_required_field(self):
        required_css_class = "bootstrap3-req"
        required_field = render_form_field("subject")
        self.assertIn(required_css_class, required_field)
        not_required_field = render_form_field("message")
        self.assertNotIn(required_css_class, not_required_field)
        # Required settings in field
        form_field = "form.subject"
        rendered = render_template_with_form(
            "{% bootstrap_field " + form_field + ' required_css_class="test-required" %}'
        )
        self.assertIn("test-required", rendered)

    def test_empty_permitted(self):
        """If a form has empty_permitted, no fields should get the CSS class for required."""
        required_css_class = "bootstrap3-req"
        form = TestForm()
        res = render_form_field("subject", {"form": form})
        self.assertIn(required_css_class, res)
        form.empty_permitted = True
        res = render_form_field("subject", {"form": form})
        self.assertNotIn(required_css_class, res)

    def test_input_group(self):
        res = render_template_with_form('{% bootstrap_field form.subject addon_before="$"  addon_after=".00" %}')
        self.assertIn('class="input-group"', res)
        self.assertIn('class="input-group-addon">$', res)
        self.assertIn('class="input-group-addon">.00', res)

    def test_input_group_addon_button(self):
        res = render_template_with_form(
            "{% bootstrap_field form.subject "
            'addon_before="$" addon_before_class="input-group-btn" '
            'addon_after=".00" addon_after_class="input-group-btn" %}'
        )
        self.assertIn('class="input-group"', res)
        self.assertIn('class="input-group-btn">$', res)
        self.assertIn('class="input-group-btn">.00', res)

    def test_size(self):
        def _test_size(param, klass):
            res = render_template_with_form('{% bootstrap_field form.subject size="' + param + '" %}')
            self.assertIn(klass, res)

        def _test_size_medium(param):
            res = render_template_with_form('{% bootstrap_field form.subject size="' + param + '" %}')
            self.assertNotIn("input-lg", res)
            self.assertNotIn("input-sm", res)
            self.assertNotIn("input-md", res)

        _test_size("sm", "input-sm")
        _test_size("small", "input-sm")
        _test_size("lg", "input-lg")
        _test_size("large", "input-lg")
        _test_size_medium("md")
        _test_size_medium("medium")
        _test_size_medium("")

    def test_datetime(self):
        field = render_form_field("datetime")
        self.assertIn("vDateField", field)
        self.assertIn("vTimeField", field)

    def test_field_same_render(self):
        context = dict(form=TestForm())
        rendered_a = render_form_field("addon", context)
        rendered_b = render_form_field("addon", context)
        self.assertEqual(rendered_a, rendered_b)

    def test_label(self):
        res = render_template_with_form('{% bootstrap_label "foobar" label_for="subject" %}')
        self.assertEqual('<label for="subject">foobar</label>', res)

    def test_attributes_consistency(self):
        form = TestForm()
        attrs = form.fields["addon"].widget.attrs.copy()
        self.assertEqual(attrs, form.fields["addon"].widget.attrs)

    def test_placeholder(self):
        res = render_template_with_form("{% bootstrap_field form.sender %}")
        self.assertIn('placeholder="Sender', res)

    def test_overwrite_placeholder(self):
        res = render_template_with_form('{% bootstrap_field form.sender placeholder="foo" %}')
        self.assertIn('placeholder="foo', res)

        # If set_placeholder is set, also consider label override for placeholder
        res = render_template_with_form('{% bootstrap_field form.sender label="foo" %}')
        self.assertNotIn("Sender", res)
        self.assertIn('placeholder="foo', res)
        self.assertIn("foo</label>", res)

    def test_overwrite_label(self):
        res = render_template_with_form('{% bootstrap_field form.sender label="foo" %}')
        self.assertNotIn("Sender", res)
        self.assertIn("foo", res)


class ComponentsTest(TestCase):
    def test_icon(self):
        res = render_template_with_form('{% bootstrap_icon "star" %}')
        self.assertEqual(res.strip(), '<span class="glyphicon glyphicon-star"></span>')
        res = render_template_with_form('{% bootstrap_icon "star" title="alpha centauri" %}')
        self.assertIn(
            res.strip(),
            [
                '<span class="glyphicon glyphicon-star" title="alpha centauri"></span>',
                '<span title="alpha centauri" class="glyphicon glyphicon-star"></span>',
            ],
        )

    def test_alert(self):
        res = render_template_with_form('{% bootstrap_alert "content" alert_type="danger" %}')
        self.assertEqual(
            res.strip(),
            '<div class="alert alert-danger alert-dismissable">'
            + '<button type="button" class="close" data-dismiss="alert" '
            + 'aria-hidden="true">'
            + "&times;</button>content</div>",
        )

    def test_alert_with_safe_html(self):
        res = render_template_with_form('{% bootstrap_alert "Foo<br>Bar"|safe %}')
        self.assertEqual(
            res.strip(),
            '<div class="alert alert-info alert-dismissable">'
            + '<button type="button" class="close" data-dismiss="alert" '
            + 'aria-hidden="true">'
            + "&times;</button>Foo<br>Bar</div>",
        )


class MessagesTest(TestCase):
    def test_messages(self):
        class FakeMessage:
            """Follows the `django.contrib.messages.storage.base.Message` API."""

            level = None
            message = None
            extra_tags = None

            def __init__(self, level, message, extra_tags=None):
                self.level = level
                self.extra_tags = extra_tags
                self.message = message

            def __str__(self):
                return self.message

        pattern = re.compile(r"\s+")
        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.WARNING, "hello")]
        res = render_template_with_form("{% bootstrap_messages messages %}", {"messages": messages})
        expected = """
    <div class="alert alert-warning alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello
    </div>
"""
        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello")]
        res = render_template_with_form("{% bootstrap_messages messages %}", {"messages": messages})
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello
    </div>
        """
        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))

        messages = [FakeMessage(None, "hello")]
        res = render_template_with_form("{% bootstrap_messages messages %}", {"messages": messages})
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello
    </div>
        """

        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello http://example.com")]
        res = render_template_with_form("{% bootstrap_messages messages %}", {"messages": messages})
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&#215;</button>
        hello http://example.com
    </div>        """
        self.assertEqual(
            re.sub(pattern, "", res).replace('rel="nofollow"', ""),
            re.sub(pattern, "", expected).replace('rel="nofollow"', ""),
        )

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello\nthere")]
        res = render_template_with_form("{% bootstrap_messages messages %}", {"messages": messages})
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello there
    </div>
        """
        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))


class UtilsTest(TestCase):
    def test_add_css_class(self):
        css_classes = "one two"
        css_class = "three four"
        classes = add_css_class(css_classes, css_class)
        self.assertEqual(classes, "one two three four")

        classes = add_css_class(css_classes, css_class, prepend=True)
        self.assertEqual(classes, "three four one two")

    def test_text_value(self):
        self.assertEqual(text_value(""), "")
        self.assertEqual(text_value(" "), " ")
        self.assertEqual(text_value(None), "")
        self.assertEqual(text_value(1), "1")

    def test_text_concat(self):
        self.assertEqual(text_concat(1, 2), "12")
        self.assertEqual(text_concat(1, 2, separator="="), "1=2")
        self.assertEqual(text_concat(None, 2, separator="="), "2")

    def test_render_tag(self):
        self.assertEqual(render_tag("span"), "<span></span>")
        self.assertEqual(render_tag("span", content="foo"), "<span>foo</span>")
        self.assertEqual(
            render_tag("span", attrs={"bar": 123}, content="foo"),
            '<span bar="123">foo</span>',
        )

    def test_url_to_attrs_dict(self):
        self.assertEqual(url_to_attrs_dict("my_link", "src"), {"src": "my_link"})
        self.assertEqual(url_to_attrs_dict({"url": "my_link"}, "src"), {"src": "my_link"})
        self.assertEqual(
            url_to_attrs_dict(
                {"url": "my_link", "crossorigin": "anonymous", "integrity": "super"},
                "src",
            ),
            {"src": "my_link", "crossorigin": "anonymous", "integrity": "super"},
        )
        with self.assertRaises(BootstrapError):
            url_to_attrs_dict(123, "src")


class ButtonTest(TestCase):
    def test_button(self):
        res = render_template_with_form("{% bootstrap_button 'button' size='lg' %}")
        self.assertEqual(res.strip(), '<button class="btn btn-default btn-lg">button</button>')
        res = render_template_with_form("{% bootstrap_button 'button' size='lg' href='#' %}")
        self.assertIn(
            res.strip(),
            '<a class="btn btn-default btn-lg" href="#">button</a><a href="#" class="btn btn-lg">button</a>',
        )


class ShowLabelTest(TestCase):
    def test_show_label(self):
        form = TestForm()
        res = render_template_with_form("{% bootstrap_form form show_label=False %}", {"form": form})
        self.assertIn("sr-only", res)

    def test_for_formset(self):
        TestFormSet = formset_factory(TestForm, extra=1)
        test_formset = TestFormSet()
        res = render_template_with_form(
            "{% bootstrap_formset formset show_label=False %}",
            {"formset": test_formset},
        )
        self.assertIn("sr-only", res)

    def test_button_with_icon(self):
        res = render_template_with_form("{% bootstrap_button 'test' icon='info-sign' %}")
        self.assertEqual(
            res.strip(),
            '<button class="btn btn-default"><span class="glyphicon glyphicon-info-sign"></span> test</button>',
        )
        res = render_template_with_form("{% bootstrap_button 'test' icon='info-sign' button_class='btn-primary' %}")
        self.assertEqual(
            res.strip(),
            '<button class="btn btn-primary"><span class="glyphicon glyphicon-info-sign"></span> test</button>',
        )
        res = render_template_with_form("{% bootstrap_button 'test' icon='info-sign' button_type='submit' %}")
        self.assertHTMLEqual(
            res,
            "<button"
            ' class="btn btn-default"'
            ' type="submit">'
            "<span"
            ' class="glyphicon glyphicon-info-sign"></span>'
            " test</button>",
        )


class ShowPlaceholderTest(TestCase):
    def test_placeholder_set_from_label(self):
        res = render_form_field("sender")
        self.assertIn('placeholder="Sender © unicode"', res)


class ShowAddonsTest(TestCase):
    def assertFieldHasAddons(self, field):
        """Assert that a given field has an after and before addon."""
        addon_before = "bf"
        addon_after = "af"

        res = render_template_with_form(
            f'{{% bootstrap_field form.{field} addon_before="{addon_before}"  addon_after="{addon_after}" %}}'
        )

        self.assertIn('class="input-group"', res)
        self.assertIn(f'class="input-group-addon">{addon_before}', res)
        self.assertIn(f'class="input-group-addon">{addon_after}', res)

    def test_show_addons_textinput(self):
        self.assertFieldHasAddons("subject")

    def test_show_addons_select(self):
        self.assertFieldHasAddons("select1")

    def test_show_addons_dateinput(self):
        self.assertFieldHasAddons("date")

    def test_show_addons_email(self):
        self.assertFieldHasAddons("sender")

    def test_show_addons_number(self):
        self.assertFieldHasAddons("number")

    def test_show_addons_url(self):
        self.assertFieldHasAddons("url")


class InlineLayoutTestCase(TestCase):
    def test_radioset_inline(self):
        form = RadioSetTestForm()
        res = render_template_with_form("{% bootstrap_form form layout='inline' %}", {"form": form})
        expected = """
            <div class="form-group bootstrap3-req">
              <label class="sr-only">Radio</label>
              <div id="id_radio">
                <div class="radio">
                  <label for="id_radio_0">
                    <input type="radio" name="radio" value="1" class="" title="" required id="id_radio_0">
                    Radio 1
                  </label>
                </div>
                <div class="radio">
                  <label for="id_radio_1">
                    <input type="radio" name="radio" value="2" class="" title="" required id="id_radio_1">
                    Radio 2
                  </label>
                </div>
              </div>
            </div>
            """
        self.assertHTMLEqual(res, expected)
        self.assertIn(
            ' <div class="radio">',
            res,
            msg="Missing relevant whitespace for inline rendering.",
        )

from django.test import TestCase

from tests.app.forms import render_template, render_template_with_form


class TemplateTest(TestCase):
    def test_empty_template(self):
        res = render_template_with_form("")
        self.assertEqual(res.strip(), "")

    def test_text_template(self):
        res = render_template_with_form("some text")
        self.assertEqual(res.strip(), "some text")

    def test_bootstrap_template(self):
        res = render_template(
            '{% extends "bootstrap3/bootstrap3.html" %}'
            + "{% block bootstrap3_content %}"
            + "test_bootstrap3_content"
            + "{% endblock %}"
        )
        self.assertIn("test_bootstrap3_content", res)

    def test_javascript_without_jquery(self):
        res = render_template_with_form("{% bootstrap_javascript jquery=0 %}")
        self.assertIn("bootstrap", res)
        self.assertNotIn("jquery", res)

    def test_javascript_with_jquery(self):
        res = render_template_with_form("{% bootstrap_javascript jquery=1 %}")
        self.assertIn("bootstrap", res)
        self.assertIn("jquery", res)

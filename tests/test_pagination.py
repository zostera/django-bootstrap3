from django.core.paginator import Paginator
from django.test import TestCase

from bootstrap3.templatetags.bootstrap3 import get_pagination_context


def context_for(page_number, object_count=100, per_page=10, **kwargs):
    """Return the pagination context for one page of a paginator over `object_count` objects."""
    paginator = Paginator(list(range(object_count)), per_page)
    return get_pagination_context(paginator.page(page_number), **kwargs)


class PaginationRangeTest(TestCase):
    """The window of page numbers shown around the current page."""

    def test_first_page_starts_the_window_at_one(self):
        context = context_for(1)
        self.assertEqual(context["current_page"], 1)
        self.assertEqual(context["first_page"], 1)
        self.assertEqual(context["pages_shown"][0], 1)
        self.assertIsNone(context["pages_back"])

    def test_a_middle_page_is_centred_in_the_window(self):
        context = context_for(5, pages_to_show=5)
        self.assertEqual(context["pages_shown"], [3, 4, 5, 6, 7])
        self.assertEqual(context["pages_back"], 1)
        self.assertEqual(context["pages_forward"], 9)

    def test_the_window_never_runs_past_the_last_page(self):
        context = context_for(10, pages_to_show=5)
        self.assertEqual(context["last_page"], 10)
        self.assertEqual(context["pages_shown"][-1], 10)
        self.assertIsNone(context["pages_forward"])

    def test_a_window_wider_than_the_paginator_shows_every_page(self):
        context = context_for(1, object_count=30, per_page=10, pages_to_show=11)
        self.assertEqual(context["pages_shown"], [1, 2, 3])
        self.assertIsNone(context["pages_back"])
        self.assertIsNone(context["pages_forward"])

    def test_pages_back_is_clamped_to_the_first_page(self):
        """first_page minus the half window would land below page 1."""
        context = context_for(4, pages_to_show=5)
        self.assertEqual(context["first_page"], 2)
        self.assertEqual(context["pages_back"], 1)

    def test_pages_forward_is_clamped_to_the_last_page(self):
        """last_page plus the half window would land beyond the final page."""
        context = context_for(7, pages_to_show=5)
        self.assertEqual(context["last_page"], 9)
        self.assertEqual(context["pages_forward"], 10)

    def test_a_single_page_paginator(self):
        context = context_for(1, object_count=5, per_page=10)
        self.assertEqual(context["num_pages"], 1)
        self.assertEqual(context["pages_shown"], [1])

    def test_pages_to_show_must_be_positive(self):
        with self.assertRaises(ValueError) as caught:
            context_for(1, pages_to_show=0)
        self.assertIn("positive integer", str(caught.exception))

    def test_pages_to_show_is_coerced_to_an_integer(self):
        """A string from a template still works."""
        self.assertEqual(context_for(5, pages_to_show="5")["pages_shown"], [3, 4, 5, 6, 7])


class PaginationUrlTest(TestCase):
    """The base URL that page links are built from."""

    def test_no_url_stays_none(self):
        self.assertIsNone(context_for(1)["bootstrap_pagination_url"])

    def test_a_plain_url_gains_a_query_separator(self):
        self.assertEqual(context_for(1, url="/list")["bootstrap_pagination_url"], "/list?")

    def test_an_existing_query_gains_an_ampersand(self):
        self.assertEqual(context_for(1, url="/list?q=x")["bootstrap_pagination_url"], "/list?q=x&")

    def test_an_existing_page_parameter_is_stripped(self):
        self.assertEqual(context_for(1, url="/list?page=3")["bootstrap_pagination_url"], "/list?")

    def test_a_trailing_page_parameter_is_stripped(self):
        self.assertEqual(context_for(1, url="/list?q=x&page=3")["bootstrap_pagination_url"], "/list?q=x&")

    def test_the_parameter_name_is_configurable(self):
        context = context_for(1, url="/list?p=3", parameter_name="p")
        self.assertEqual(context["bootstrap_pagination_url"], "/list?")
        self.assertEqual(context["parameter_name"], "p")

    def test_extra_is_appended(self):
        self.assertEqual(context_for(1, url="/list", extra="q=x")["bootstrap_pagination_url"], "/list?q=x&")

    def test_extra_without_a_url_still_produces_a_query(self):
        self.assertEqual(context_for(1, extra="q=x")["bootstrap_pagination_url"], "?q=x&")


class PaginationCssClassTest(TestCase):
    """The size modifier on the pagination element."""

    def test_default_size_has_no_modifier(self):
        self.assertEqual(context_for(1)["pagination_css_classes"], "pagination")

    def test_small(self):
        self.assertEqual(context_for(1, size="small")["pagination_css_classes"], "pagination pagination-sm")

    def test_large(self):
        self.assertEqual(context_for(1, size="large")["pagination_css_classes"], "pagination pagination-lg")

    def test_an_unknown_size_is_ignored(self):
        self.assertEqual(context_for(1, size="enormous")["pagination_css_classes"], "pagination")


class PaginationTagTest(TestCase):
    """The template tags that render pagination."""

    def render(self, template, context=None):
        from django.template import Context, Template

        return Template("{% load bootstrap3 %}" + template).render(Context(context or {}))

    def test_bootstrap_pagination_renders_the_page_links(self):
        paginator = Paginator(list(range(100)), 10)
        html = self.render("{% bootstrap_pagination page %}", {"page": paginator.page(5)})
        self.assertIn('class="pagination"', html)
        self.assertIn(">5<", html)

    def test_bootstrap_pagination_passes_its_keyword_arguments_through(self):
        paginator = Paginator(list(range(100)), 10)
        html = self.render(
            '{% bootstrap_pagination page size="large" url="/list" %}',
            {"page": paginator.page(1)},
        )
        self.assertIn("pagination-lg", html)
        self.assertIn("/list?", html)

    def test_bootstrap_url_replace_param(self):
        self.assertEqual(
            self.render('{% bootstrap_url_replace_param "/list?page=2" "page" 5 %}'),
            "/list?page=5",
        )

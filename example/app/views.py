from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from .forms import ContactForm, ContactFormSet, FilesForm


# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField:
    storage = default_storage


fieldfile = FieldFile(None, FakeField, "dummy.txt")


class HomePageView(TemplateView):
    template_name = "app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, "hello http://example.com")
        return context


class DefaultFormsetView(FormView):
    template_name = "app/formset.html"
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = "app/form.html"
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = "app/form_by_field.html"
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = "app/form_horizontal.html"
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = "app/form_inline.html"
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = "app/form_with_files.html"
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["layout"] = self.request.GET.get("layout", "vertical")
        return context

    def get_initial(self):
        return {"file4": fieldfile}


class PaginationView(TemplateView):
    template_name = "app/pagination.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        num_lines = 200
        lines = []
        for i in range(1, num_lines + 1):
            lines.append(f"Line {i}")
        paginator = Paginator(lines, 10)
        page = self.request.GET.get("page")
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context["lines"] = show_lines
        return context


class MiscView(TemplateView):
    template_name = "app/misc.html"

from django.views.generic import FormView
from django.views.generic.base import TemplateView

from .forms import ContactForm


class HomePageView(TemplateView):
    template_name = 'demo/home.html'


class FormView(FormView):
    template_name = 'demo/form.html'
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = 'demo/form_horizontal.html'
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = 'demo/form_inline.html'
    form_class = ContactForm
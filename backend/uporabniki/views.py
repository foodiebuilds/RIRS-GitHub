from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import RegistracijaForm


class DomovView(LoginRequiredMixin, TemplateView):
    template_name = "uporabniki/domov.html"


class RegistracijaView(CreateView):
    form_class = RegistracijaForm
    template_name = "uporabniki/registracija.html"
    success_url = reverse_lazy("prijava")

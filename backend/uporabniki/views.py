from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DomovView(LoginRequiredMixin, TemplateView):
    template_name = "uporabniki/domov.html"

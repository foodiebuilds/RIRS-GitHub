from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import PrijavaForm

urlpatterns = [
    path("", views.DomovView.as_view(), name="domov"),
    path(
        "prijava/",
        auth_views.LoginView.as_view(
            template_name="uporabniki/prijava.html", authentication_form=PrijavaForm
        ),
        name="prijava",
    ),
    path("odjava/", auth_views.LogoutView.as_view(), name="odjava"),
    path("registracija/", views.RegistracijaView.as_view(), name="registracija"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("prehrana/", views.prehrana, name="prehrana"),
    path("prehrana/<int:sportnik_id>/", views.prehrana_sportnika, name="prehrana_sportnika"),
    path("prehrana/voda/", views.dodaj_vodo, name="dodaj_vodo"),
    path("prehrana/cilj/", views.nastavi_cilj, name="nastavi_cilj"),
]

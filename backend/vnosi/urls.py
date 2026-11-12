from django.urls import path

from . import views

urlpatterns = [
    path("prehrana/", views.prehrana, name="prehrana"),
    path("prehrana/<int:sportnik_id>/", views.prehrana_sportnika, name="prehrana_sportnika"),
    path("prehrana/voda/", views.dodaj_vodo, name="dodaj_vodo"),
    path("prehrana/cilj/", views.nastavi_cilj, name="nastavi_cilj"),
    path("casovnica/", views.casovnica, name="casovnica"),
    path("casovnica/<int:sportnik_id>/", views.casovnica_sportnika, name="casovnica_sportnika"),
    path("casovnica/<int:sportnik_id>/komentar/", views.dodaj_komentar, name="dodaj_komentar"),
    path("casovnica/pocutje/", views.dodaj_pocutje, name="dodaj_pocutje"),
    path("casovnica/teza/", views.dodaj_tezo, name="dodaj_tezo"),
]

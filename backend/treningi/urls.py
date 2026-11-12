from django.urls import path

from . import views

urlpatterns = [
    path("treningi/", views.treningi, name="treningi"),
    path("treningi/kopiraj/<int:kopiraj>/", views.treningi, name="kopiraj_trening"),
    path("statistika/misice/", views.zemljevid_misic, name="zemljevid_misic"),
    path("statistika/misice/<int:sportnik_id>/", views.zemljevid_misic, name="zemljevid_misic_sportnika"),
]

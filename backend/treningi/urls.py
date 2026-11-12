from django.urls import path

from . import views

urlpatterns = [
    path("treningi/", views.treningi, name="treningi"),
    path("treningi/kopiraj/<int:kopiraj>/", views.treningi, name="kopiraj_trening"),
]

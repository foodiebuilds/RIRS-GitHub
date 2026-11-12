from django.urls import path

from . import views

urlpatterns = [
    path("treningi/", views.treningi, name="treningi"),
]

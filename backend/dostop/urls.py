from django.urls import path

from . import views

urlpatterns = [
    path("dostop/", views.moj_dostop, name="moj_dostop"),
]

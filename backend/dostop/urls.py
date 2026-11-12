from django.urls import path

from . import views

urlpatterns = [
    path("dostop/", views.moj_dostop, name="moj_dostop"),
    path("dostop/<int:pk>/preklici/", views.preklici, name="preklici_dostop"),
    path("moji-sportniki/", views.moji_sportniki, name="moji_sportniki"),
    path(
        "moji-sportniki/povabilo/<int:pk>/<str:odgovor>/",
        views.odgovori_na_povabilo,
        name="odgovori_na_povabilo",
    ),
]

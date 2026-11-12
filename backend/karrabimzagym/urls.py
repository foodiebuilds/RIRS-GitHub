from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("uporabniki.urls")),
    path("", include("dostop.urls")),
    path("", include("vnosi.urls")),
    path("", include("treningi.urls")),
]

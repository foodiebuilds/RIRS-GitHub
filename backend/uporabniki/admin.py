from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Uporabnik


@admin.register(Uporabnik)
class UporabnikAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Podatki uporabnika", {"fields": ("ime",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Podatki uporabnika", {"fields": ("ime", "email")}),)
    list_display = ("username", "ime", "email", "is_active", "is_staff")

from django.contrib import admin

from .models import Misica, Vaja, VajaMisica


class VajaMisicaInline(admin.TabularInline):
    model = VajaMisica
    extra = 1


@admin.register(Vaja)
class VajaAdmin(admin.ModelAdmin):
    inlines = [VajaMisicaInline]


@admin.register(Misica)
class MisicaAdmin(admin.ModelAdmin):
    list_display = ("ime", "pogled")

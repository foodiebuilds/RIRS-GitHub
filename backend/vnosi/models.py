from django.conf import settings
from django.db import models
from django.utils import timezone


class Vnos(models.Model):
    """En vnos na časovnici: voda (ml), obrok (kcal + opis), počutje (1–5) ali teža (kg) (docs/03)."""

    class Tip(models.TextChoices):
        VODA = "VODA", "voda"
        OBROK = "OBROK", "obrok"
        POCUTJE = "POCUTJE", "počutje"
        TEZA = "TEZA", "teža"

    uporabnik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vnosi")
    cas = models.DateTimeField(default=timezone.now)
    tip = models.CharField(max_length=10, choices=Tip)
    kolicina = models.FloatField()
    opis = models.CharField(max_length=200, blank=True)

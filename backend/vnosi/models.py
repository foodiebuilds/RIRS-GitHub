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


class DnevniCilj(models.Model):
    """Dnevni cilj kalorij in vode (docs/03, ADR-0003). Stari cilji se hranijo za pretekle dni."""

    class Status(models.TextChoices):
        PREDLAGAN = "PREDLAGAN", "predlagan"
        AKTIVEN = "AKTIVEN", "aktiven"
        ZAVRNJEN = "ZAVRNJEN", "zavrnjen"
        ZAMENJAN = "ZAMENJAN", "zamenjan"

    sportnik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cilji")
    avtor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="avtor_ciljev")
    kcal = models.PositiveIntegerField()
    voda_ml = models.PositiveIntegerField()
    velja_od = models.DateField()
    status = models.CharField(max_length=10, choices=Status)


def cilj_za_dan(sportnik, dan):
    """Cilj, ki je veljal na izbrani dan: zadnji sprejet cilj z velja_od do tega dne (ali None)."""
    return (
        DnevniCilj.objects.filter(
            sportnik=sportnik,
            status__in=[DnevniCilj.Status.AKTIVEN, DnevniCilj.Status.ZAMENJAN],
            velja_od__lte=dan,
        )
        .order_by("-velja_od", "-id")
        .first()
    )

from django.conf import settings
from django.db import models


class Dostop(models.Model):
    """Kdo ima dostop do športnikovih podatkov in v kateri vlogi (docs/03).

    Če je ista oseba trener in svetovalec, ima dve vrstici.
    """

    class Vrsta(models.TextChoices):
        TRENER = "TRENER", "trener"
        PREHRANSKI_SVETOVALEC = "PREHRANSKI_SVETOVALEC", "prehranski svetovalec"

    class Status(models.TextChoices):
        POVABLJEN = "POVABLJEN", "povabljen"
        AKTIVEN = "AKTIVEN", "aktiven"
        PREKLICAN = "PREKLICAN", "preklican"

    sportnik = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dani_dostopi"
    )
    strokovnjak = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="prejeti_dostopi"
    )
    vrsta = models.CharField(max_length=30, choices=Vrsta)
    status = models.CharField(max_length=20, choices=Status, default=Status.POVABLJEN)
    ustvarjen = models.DateTimeField(auto_now_add=True)

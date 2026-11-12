from django.conf import settings
from django.db import models
from django.utils import timezone


class Misica(models.Model):
    """Večja mišična skupina na zemljevidu mišic (docs/03). Seznam ureja administrator."""

    class Pogled(models.TextChoices):
        SPREDAJ = "SPREDAJ", "spredaj"
        ZADAJ = "ZADAJ", "zadaj"

    ime = models.CharField(max_length=50, unique=True)
    pogled = models.CharField(max_length=10, choices=Pogled)
    # Mišična skupina na sliki obsega več delov telesa iz knjižnice body-muscles.
    oznake = models.CharField(
        max_length=500, blank=True, help_text="Oznake mišic v knjižnici body-muscles, ločene z vejico."
    )

    class Meta:
        verbose_name = "mišica"
        verbose_name_plural = "mišice"
        ordering = ["ime"]

    def __str__(self):
        return self.ime


class Vaja(models.Model):
    """Vaja s seznama, ki ga ureja administrator (docs/03)."""

    ime = models.CharField(max_length=100, unique=True)
    opis = models.TextField(blank=True)
    misice = models.ManyToManyField(Misica, through="VajaMisica")

    class Meta:
        verbose_name = "vaja"
        verbose_name_plural = "vaje"
        ordering = ["ime"]

    def __str__(self):
        return self.ime


class VajaMisica(models.Model):
    """Katere mišice vaja obremeni. Glavna šteje 1, pomožna 0,5 (docs/03)."""

    class Tip(models.TextChoices):
        GLAVNA = "GLAVNA", "glavna"
        POMOZNA = "POMOZNA", "pomožna"

    vaja = models.ForeignKey(Vaja, on_delete=models.CASCADE)
    misica = models.ForeignKey(Misica, on_delete=models.CASCADE)
    tip = models.CharField(max_length=10, choices=Tip)

    class Meta:
        verbose_name = "mišica vaje"
        verbose_name_plural = "mišice vaje"
        constraints = [models.UniqueConstraint(fields=["vaja", "misica"], name="vaja_misica_enkrat")]


class Trening(models.Model):
    """Dejansko opravljen trening (docs/03). Povezava na planirani trening se doda s plani (US-06)."""

    uporabnik = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="treningi")
    zacetek = models.DateTimeField(default=timezone.now)
    trajanje_min = models.PositiveIntegerField()
    porabljene_kcal = models.PositiveIntegerField()
    opomba = models.CharField(max_length=200, blank=True)


class Serija(models.Model):
    """Ena serija vaje na treningu (docs/03)."""

    trening = models.ForeignKey(Trening, on_delete=models.CASCADE, related_name="serije")
    vaja = models.ForeignKey(Vaja, on_delete=models.PROTECT)
    zaporedna_st = models.PositiveIntegerField()
    ponovitve = models.PositiveIntegerField()
    teza_kg = models.FloatField()

    class Meta:
        ordering = ["zaporedna_st"]

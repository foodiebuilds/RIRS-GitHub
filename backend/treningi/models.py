from django.db import models


class Misica(models.Model):
    """Večja mišična skupina na zemljevidu mišic (docs/03). Seznam ureja administrator."""

    class Pogled(models.TextChoices):
        SPREDAJ = "SPREDAJ", "spredaj"
        ZADAJ = "ZADAJ", "zadaj"

    ime = models.CharField(max_length=50, unique=True)
    pogled = models.CharField(max_length=10, choices=Pogled)

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

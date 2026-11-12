from django.contrib.auth.models import AbstractUser
from django.db import models


class Uporabnik(AbstractUser):
    """Vsak uporabnik je športnik (docs/03).

    Polja iz podatkovnega modela so preslikana na polja Djanga:
    uporabnisko_ime = username, geslo_hash = password, ustvarjen = date_joined,
    sistemska_vloga ADMIN = is_staff, blokiran račun = is_active False.
    """

    ime = models.CharField("ime", max_length=150)
    email = models.EmailField(
        "e-pošta", unique=True, error_messages={"unique": "Uporabnik s tem e-naslovom že obstaja."}
    )

    REQUIRED_FIELDS = ["email", "ime"]

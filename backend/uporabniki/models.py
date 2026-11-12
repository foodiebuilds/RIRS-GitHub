from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower


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

    class Meta(AbstractUser.Meta):
        # Tudi računi iz admina in createsuperuser: ista e-pošta z drugimi velikimi črkami je zasedena (US-01 AC2).
        constraints = [
            models.UniqueConstraint(
                Lower("email"), name="email_enolicen", violation_error_message="Uporabnik s tem e-naslovom že obstaja."
            )
        ]

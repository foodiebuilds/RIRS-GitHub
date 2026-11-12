from django.contrib.auth.backends import ModelBackend

from .models import Uporabnik


class PrijavaZEposto(ModelBackend):
    """Prijava z e-pošto in geslom. Prijavo z uporabniškim imenom opravi ModelBackend."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        uporabnik = Uporabnik.objects.filter(email__iexact=username).first()
        # user_can_authenticate zavrne blokiran račun (is_active = False).
        if uporabnik and uporabnik.check_password(password) and self.user_can_authenticate(uporabnik):
            return uporabnik
        return None

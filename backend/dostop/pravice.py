from .models import Dostop

# Katere podatke športnika vidi strokovnjak glede na vrsto dostopa (docs/02, US-05 AC4).
# "treningi" vključuje vaje, serije, porabljene kalorije in statistiko treningov.
PODATKI = {
    Dostop.Vrsta.TRENER: {"treningi", "plani", "pocutje", "teza"},
    Dostop.Vrsta.PREHRANSKI_SVETOVALEC: {"voda", "obroki", "kcal_treningov", "cilji", "pocutje", "teza"},
}
VSI_PODATKI = PODATKI[Dostop.Vrsta.TRENER] | PODATKI[Dostop.Vrsta.PREHRANSKI_SVETOVALEC]


def vidni_podatki(uporabnik, sportnik):
    """Podatki športnika, ki jih uporabnik sme videti. Lastnik vidi vse, drugi samo z aktivnim dostopom."""
    if uporabnik == sportnik:
        return VSI_PODATKI
    vrste = Dostop.objects.filter(
        sportnik=sportnik, strokovnjak=uporabnik, status=Dostop.Status.AKTIVEN
    ).values_list("vrsta", flat=True)
    vidni = set()
    for vrsta in vrste:
        vidni |= PODATKI[vrsta]
    return vidni

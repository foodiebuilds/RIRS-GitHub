from collections import Counter

from .models import Misica, Serija, VajaMisica

TOCKE = {VajaMisica.Tip.GLAVNA: 1, VajaMisica.Tip.POMOZNA: 0.5}


def obremenitev_misic(uporabnik, od, do):
    """Obremenitev vsake mišice v obdobju od–do (vključno) na lestvici 0–10 (docs/02 f3, US-03).

    Vsaka serija prišteje 1 glavni mišici vaje in 0,5 vsaki pomožni. Najbolj obremenjena
    mišica dobi 10, ostale sorazmerno manj, zaokroženo navzgor od polovice; trenirana mišica
    ima najmanj 1. Netrenirana mišica ima 0. Vrne {mišica: vrednost} za vse mišice.
    """
    serije_po_vajah = Counter(
        Serija.objects.filter(
            trening__uporabnik=uporabnik, trening__zacetek__date__gte=od, trening__zacetek__date__lte=do
        ).values_list("vaja_id", flat=True)
    )
    tocke = Counter()
    for vm in VajaMisica.objects.filter(vaja_id__in=serije_po_vajah):
        tocke[vm.misica_id] += serije_po_vajah[vm.vaja_id] * TOCKE[vm.tip]
    najvec = max(tocke.values(), default=0)
    obremenitev = {}
    for misica in Misica.objects.all():
        if tocke[misica.id] == 0:
            obremenitev[misica] = 0
        else:
            obremenitev[misica] = max(1, int(tocke[misica.id] / najvec * 10 + 0.5))
    return obremenitev

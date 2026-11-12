from django.utils import timezone

from .models import Vnos

# Kateri podatek (iz dostop.pravice) je vnos posamezne vrste.
PODATEK_VNOSA = {
    Vnos.Tip.VODA: "voda",
    Vnos.Tip.OBROK: "obroki",
    Vnos.Tip.POCUTJE: "pocutje",
    Vnos.Tip.TEZA: "teza",
}


def dnevi_casovnice(sportnik, vidni):
    """Vnosi športnika, ki jih sme gledalec videti (vidni = množica podatkov iz vidni_podatki).

    Vrne [(dan, [postavka, ...]), ...]: najnovejši dan najprej, znotraj dneva po času.
    Postavka je {"cas", "trening"} ali {"cas", "vnos"}; pri treningu "samo_kcal" pove,
    da gledalec vidi samo porabljene kalorije (prehranski svetovalec).
    """
    postavke = []
    if {"treningi", "kcal_treningov"} & vidni:
        for t in sportnik.treningi.prefetch_related("serije__vaja"):
            postavke.append({"cas": t.zacetek, "trening": t, "samo_kcal": "treningi" not in vidni})
    tipi = [tip for tip, podatek in PODATEK_VNOSA.items() if podatek in vidni]
    for v in sportnik.vnosi.filter(tip__in=tipi):
        postavke.append({"cas": v.cas, "vnos": v})
    postavke.sort(key=lambda p: p["cas"])
    dnevi = {}
    for p in postavke:
        dnevi.setdefault(timezone.localdate(p["cas"]), []).append(p)
    return sorted(dnevi.items(), key=lambda d: d[0], reverse=True)

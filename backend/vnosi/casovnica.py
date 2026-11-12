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
    Postavka je {"cas", "trening", "samo_kcal", "komentarji"} ali {"cas", "vnos", "komentarji"};
    "samo_kcal" pove, da gledalec pri treningu vidi samo porabljene kalorije (prehranski svetovalec).
    """
    postavke = []
    if {"treningi", "kcal_treningov"} & vidni:
        for t in sportnik.treningi.prefetch_related("serije__vaja", "komentarji__avtor"):
            postavke.append(
                {"cas": t.zacetek, "trening": t, "samo_kcal": "treningi" not in vidni, "komentarji": t.komentarji.all()}
            )
    tipi = [tip for tip, podatek in PODATEK_VNOSA.items() if podatek in vidni]
    for v in sportnik.vnosi.filter(tip__in=tipi).prefetch_related("komentarji__avtor"):
        postavke.append({"cas": v.cas, "vnos": v, "komentarji": v.komentarji.all()})
    postavke.sort(key=lambda p: p["cas"])
    dnevi = {}
    for p in postavke:
        dnevi.setdefault(timezone.localdate(p["cas"]), []).append(p)
    return sorted(dnevi.items(), key=lambda d: d[0], reverse=True)


def vidi_postavko(vidni, trening=None, vnos=None):
    """Ali gledalec s temi vidnimi podatki vidi ta trening oziroma vnos."""
    if trening is not None:
        return bool({"treningi", "kcal_treningov"} & vidni)
    return PODATEK_VNOSA[vnos.tip] in vidni

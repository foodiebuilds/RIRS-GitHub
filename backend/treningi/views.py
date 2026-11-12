from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ObdobjeForm, SerijaFormSet, TreningForm
from .models import Serija, Trening
from .zemljevid import obremenitev_misic


@login_required
def treningi(request, kopiraj=None):
    """Vnos novega treninga z vajami in serijami ter seznam preteklih treningov.

    Pri »Kopiraj trening« (kopiraj = id treninga) je obrazec izpolnjen s podatki tega treninga.
    """
    trening_zacetno, serije_zacetno = None, None
    if kopiraj is not None:
        vzor = get_object_or_404(Trening, pk=kopiraj, uporabnik=request.user)
        trening_zacetno = {"trajanje_min": vzor.trajanje_min, "porabljene_kcal": vzor.porabljene_kcal}
        serije_zacetno = [
            {"vaja": s.vaja_id, "ponovitve": s.ponovitve, "teza_kg": s.teza_kg} for s in vzor.serije.all()
        ]
    trening_form = TreningForm(request.POST or None, initial=trening_zacetno)
    serije_formset = SerijaFormSet(request.POST or None, prefix="serije", initial=serije_zacetno)
    if request.method == "POST" and trening_form.is_valid() and serije_formset.is_valid():
        with transaction.atomic():
            trening = trening_form.save(commit=False)
            trening.uporabnik = request.user
            trening.save()
            vrstice = [f.cleaned_data for f in serije_formset if f.cleaned_data and not f.cleaned_data["DELETE"]]
            for st, v in enumerate(vrstice, start=1):
                Serija.objects.create(
                    trening=trening, zaporedna_st=st, vaja=v["vaja"], ponovitve=v["ponovitve"], teza_kg=v["teza_kg"]
                )
        return redirect("treningi")
    pretekli = request.user.treningi.order_by("-zacetek", "-id").prefetch_related("serije__vaja")
    return render(
        request,
        "treningi/treningi.html",
        {"trening_form": trening_form, "serije_formset": serije_formset, "pretekli": pretekli},
    )


@login_required
def zemljevid_misic(request):
    """Zemljevid obremenitve mišic za zadnjih 7 dni (privzeto), zadnjih 30 dni ali poljubno obdobje."""
    danes = timezone.localdate()
    dni = 30 if request.GET.get("dni") == "30" else 7
    od, do = danes - timedelta(days=dni - 1), danes
    obdobje_form = ObdobjeForm(request.GET if "od" in request.GET else None)
    if obdobje_form.is_valid():
        od, do = obdobje_form.cleaned_data["od"], obdobje_form.cleaned_data["do"]
    obremenitev = obremenitev_misic(request.user, od, do)
    # Stanje za knjižnico body-muscles: vsaka oznaka trenirane mišice dobi vrednost mišice.
    stanje = {
        oznaka: {"intensity": vrednost, "selected": False}
        for misica, vrednost in obremenitev.items()
        if vrednost > 0
        for oznaka in (o.strip() for o in misica.oznake.split(","))
        if oznaka
    }
    trenirane = sorted(
        ((m, v) for m, v in obremenitev.items() if v > 0), key=lambda mv: (-mv[1], mv[0].ime)
    )
    return render(
        request,
        "treningi/zemljevid_misic.html",
        {
            "od": od,
            "do": do,
            "obdobje_form": obdobje_form,
            "stanje": stanje,
            "najbolj_obremenjene": trenirane[:5],
            "netrenirane": [m for m, v in obremenitev.items() if v == 0],
            "ni_treningov": not request.user.treningi.filter(
                zacetek__date__gte=od, zacetek__date__lte=do
            ).exists(),
        },
    )

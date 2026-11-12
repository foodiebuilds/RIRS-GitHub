from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import SerijaFormSet, TreningForm
from .models import Serija, Trening


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

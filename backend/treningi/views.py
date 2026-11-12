from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import SerijaFormSet, TreningForm
from .models import Serija


@login_required
def treningi(request):
    """Vnos novega treninga z vajami in serijami."""
    trening_form = TreningForm(request.POST or None)
    serije_formset = SerijaFormSet(request.POST or None, prefix="serije")
    if request.method == "POST" and trening_form.is_valid() and serije_formset.is_valid():
        with transaction.atomic():
            trening = trening_form.save(commit=False)
            trening.uporabnik = request.user
            trening.save()
            vrstice = [f.cleaned_data for f in serije_formset if f.cleaned_data]
            for st, vrstica in enumerate(vrstice, start=1):
                Serija.objects.create(trening=trening, zaporedna_st=st, **vrstica)
        return redirect("treningi")
    return render(
        request, "treningi/treningi.html", {"trening_form": trening_form, "serije_formset": serije_formset}
    )

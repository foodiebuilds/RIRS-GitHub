from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import PovabiloForm
from .models import Dostop


@login_required
def moj_dostop(request):
    """Športnik povabi trenerja ali prehranskega svetovalca in vidi, komu je dal dostop."""
    form = PovabiloForm(request.POST or None, sportnik=request.user)
    if request.method == "POST" and form.is_valid():
        for vrsta in form.vrste():
            Dostop.objects.create(sportnik=request.user, strokovnjak=form.strokovnjak, vrsta=vrsta)
        return redirect("moj_dostop")
    dostopi = request.user.dani_dostopi.exclude(status=Dostop.Status.PREKLICAN).select_related("strokovnjak")
    return render(request, "dostop/moj_dostop.html", {"form": form, "dostopi": dostopi})


@login_required
@require_POST
def preklici(request, pk):
    """Športnik prekliče povabilo ali dostop."""
    dostop = get_object_or_404(
        Dostop, pk=pk, sportnik=request.user, status__in=[Dostop.Status.POVABLJEN, Dostop.Status.AKTIVEN]
    )
    dostop.status = Dostop.Status.PREKLICAN
    dostop.save()
    return redirect("moj_dostop")


@login_required
def moji_sportniki(request):
    """Povabila, ki jih je uporabnik dobil, in športniki, ki so mu dali dostop."""
    povabila = request.user.prejeti_dostopi.filter(status=Dostop.Status.POVABLJEN).select_related("sportnik")
    aktivni = (
        request.user.prejeti_dostopi.filter(status=Dostop.Status.AKTIVEN)
        .select_related("sportnik")
        .order_by("sportnik__ime", "sportnik_id", "vrsta")
    )
    return render(request, "dostop/moji_sportniki.html", {"povabila": povabila, "aktivni": aktivni})


@login_required
@require_POST
def odgovori_na_povabilo(request, pk, odgovor):
    """Povabljeni povabilo sprejme (AKTIVEN) ali zavrne (PREKLICAN)."""
    if odgovor not in ("sprejmi", "zavrni"):
        raise Http404
    dostop = get_object_or_404(Dostop, pk=pk, strokovnjak=request.user, status=Dostop.Status.POVABLJEN)
    dostop.status = Dostop.Status.AKTIVEN if odgovor == "sprejmi" else Dostop.Status.PREKLICAN
    dostop.save()
    return redirect("moji_sportniki")

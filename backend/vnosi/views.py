from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CiljForm, ObrokForm
from .models import DnevniCilj, Vnos, cilj_za_dan

VODA_GUMB_ML = 250


@login_required
def prehrana(request):
    """Voda in obroki za danes; obrazec za obrok."""
    obrok_form = ObrokForm(request.POST or None)
    if request.method == "POST" and obrok_form.is_valid():
        Vnos.objects.create(
            uporabnik=request.user,
            tip=Vnos.Tip.OBROK,
            kolicina=obrok_form.cleaned_data["kcal"],
            opis=obrok_form.cleaned_data["opis"],
        )
        return redirect("prehrana")
    vnosi = request.user.vnosi.filter(
        tip__in=[Vnos.Tip.VODA, Vnos.Tip.OBROK], cas__date=timezone.localdate()
    ).order_by("cas")
    return render(
        request,
        "vnosi/prehrana.html",
        {
            "vnosi": vnosi,
            "obrok_form": obrok_form,
            "cilj": cilj_za_dan(request.user, timezone.localdate()),
            "cilj_form": CiljForm(),
        },
    )


@login_required
@require_POST
def dodaj_vodo(request):
    Vnos.objects.create(uporabnik=request.user, tip=Vnos.Tip.VODA, kolicina=VODA_GUMB_ML)
    return redirect("prehrana")


@login_required
@require_POST
def nastavi_cilj(request):
    """Športnik si nastavi cilj, ki velja od danes. Prejšnji aktivni cilj ostane shranjen kot ZAMENJAN."""
    form = CiljForm(request.POST)
    if form.is_valid():
        with transaction.atomic():
            request.user.cilji.filter(status=DnevniCilj.Status.AKTIVEN).update(status=DnevniCilj.Status.ZAMENJAN)
            DnevniCilj.objects.create(
                sportnik=request.user,
                avtor=request.user,
                kcal=form.cleaned_data["kcal"],
                voda_ml=form.cleaned_data["voda_ml"],
                velja_od=timezone.localdate(),
                status=DnevniCilj.Status.AKTIVEN,
            )
    return redirect("prehrana")

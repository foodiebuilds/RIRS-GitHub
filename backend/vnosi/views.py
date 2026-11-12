from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q, Sum
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from dostop.pravice import vidni_podatki
from uporabniki.models import Uporabnik

from .forms import CiljForm, ObrokForm
from .models import DnevniCilj, Vnos, cilj_za_dan

VODA_GUMB_ML = 250
PRETEKLI_DNEVI = 7


def litri(ml):
    return f"{ml / 1000:g}".replace(".", ",") + " l"


def kalorije(kcal):
    return f"{kcal:g} kcal"


def napredek(vneseno, cilj, oblika):
    """Npr. »1,5 l od 2,5 l, manjka 1 l«."""
    if cilj is None:
        return f"{oblika(vneseno)} (cilj ni nastavljen)"
    return f"{oblika(vneseno)} od {oblika(cilj)}, manjka {oblika(max(cilj - vneseno, 0))}"


def pregled_dneva(sportnik, dan):
    """Vnos vode in kalorij na izbrani dan v primerjavi s ciljem, ki je veljal tisti dan."""
    vsote = sportnik.vnosi.filter(cas__date=dan).aggregate(
        voda=Sum("kolicina", filter=Q(tip=Vnos.Tip.VODA), default=0),
        kcal=Sum("kolicina", filter=Q(tip=Vnos.Tip.OBROK), default=0),
    )
    cilj = cilj_za_dan(sportnik, dan)
    return {
        "dan": dan,
        "voda": napredek(vsote["voda"], cilj and cilj.voda_ml, litri),
        "kcal": napredek(vsote["kcal"], cilj and cilj.kcal, kalorije),
    }


def podatki_prehrane(sportnik):
    """Današnji vnosi vode in obrokov, veljavni cilj, napredek danes in zadnjih 7 dni."""
    danes = timezone.localdate()
    return {
        "sportnik": sportnik,
        "vnosi": sportnik.vnosi.filter(tip__in=[Vnos.Tip.VODA, Vnos.Tip.OBROK], cas__date=danes).order_by("cas"),
        "cilj": cilj_za_dan(sportnik, danes),
        "danes": pregled_dneva(sportnik, danes),
        "pretekli_dnevi": [pregled_dneva(sportnik, danes - timedelta(days=i)) for i in range(1, PRETEKLI_DNEVI + 1)],
    }


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
    return render(
        request,
        "vnosi/prehrana.html",
        {**podatki_prehrane(request.user), "obrok_form": obrok_form, "cilj_form": CiljForm()},
    )


@login_required
def prehrana_sportnika(request, sportnik_id):
    """Pregled prehrane športnika za prehranskega svetovalca (samo branje, US-05 AC4)."""
    sportnik = get_object_or_404(Uporabnik, pk=sportnik_id)
    if sportnik == request.user:
        return redirect("prehrana")
    if "cilji" not in vidni_podatki(request.user, sportnik):
        raise Http404
    return render(request, "vnosi/prehrana.html", podatki_prehrane(sportnik))


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

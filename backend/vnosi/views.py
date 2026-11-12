from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import ObrokForm
from .models import Vnos

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
    return render(request, "vnosi/prehrana.html", {"vnosi": vnosi, "obrok_form": obrok_form})


@login_required
@require_POST
def dodaj_vodo(request):
    Vnos.objects.create(uporabnik=request.user, tip=Vnos.Tip.VODA, kolicina=VODA_GUMB_ML)
    return redirect("prehrana")

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

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

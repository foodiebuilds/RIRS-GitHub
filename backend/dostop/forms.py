from django import forms

from uporabniki.models import Uporabnik

from .models import Dostop


class PovabiloForm(forms.Form):
    OBOJE = "OBOJE"
    VRSTE = Dostop.Vrsta.choices + [(OBOJE, "trener in prehranski svetovalec")]

    uporabnisko_ime = forms.CharField(label="Uporabniško ime")
    vrsta = forms.ChoiceField(label="Vrsta dostopa", choices=VRSTE)

    def __init__(self, *args, sportnik, **kwargs):
        super().__init__(*args, **kwargs)
        self.sportnik = sportnik

    def clean_uporabnisko_ime(self):
        ime = self.cleaned_data["uporabnisko_ime"]
        strokovnjak = Uporabnik.objects.filter(username=ime).first()
        if strokovnjak is None:
            raise forms.ValidationError("Uporabnik s tem uporabniškim imenom ne obstaja.")
        if strokovnjak == self.sportnik:
            raise forms.ValidationError("Sebe ne moreš povabiti.")
        self.strokovnjak = strokovnjak
        return ime

    def vrste(self):
        vrsta = self.cleaned_data["vrsta"]
        return [Dostop.Vrsta.TRENER, Dostop.Vrsta.PREHRANSKI_SVETOVALEC] if vrsta == self.OBOJE else [vrsta]

    def clean(self):
        if not self.errors:
            for vrsta in self.vrste():
                obstaja = (
                    Dostop.objects.filter(sportnik=self.sportnik, strokovnjak=self.strokovnjak, vrsta=vrsta)
                    .exclude(status=Dostop.Status.PREKLICAN)
                    .exists()
                )
                if obstaja:
                    raise forms.ValidationError("Ta uporabnik je za to vrsto dostopa že povabljen ali ima dostop.")
        return self.cleaned_data

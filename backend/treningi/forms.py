from django import forms

from .models import Trening, Vaja


class TreningForm(forms.ModelForm):
    class Meta:
        model = Trening
        fields = ["trajanje_min", "porabljene_kcal"]
        labels = {"trajanje_min": "Trajanje (min)", "porabljene_kcal": "Porabljene kcal"}


class SerijaForm(forms.Form):
    vaja = forms.ModelChoiceField(label="Vaja", queryset=Vaja.objects.all(), empty_label="– izberi vajo –")
    ponovitve = forms.IntegerField(label="Ponovitve", min_value=1, max_value=1000)
    teza_kg = forms.FloatField(label="Teža (kg)", min_value=0)


# Prazne vrstice se ne shranijo; vsaj ena serija je obvezna.
# Pri kopiranem treningu lahko serijo odstraniš s kljukico »Odstrani«.
SerijaFormSet = forms.formset_factory(SerijaForm, extra=8, min_num=1, validate_min=True, can_delete=True)


class ObdobjeForm(forms.Form):
    od = forms.DateField(label="Od", widget=forms.DateInput(attrs={"type": "date"}))
    do = forms.DateField(label="Do", widget=forms.DateInput(attrs={"type": "date"}))

    def clean(self):
        podatki = super().clean()
        if podatki.get("od") and podatki.get("do") and podatki["od"] > podatki["do"]:
            raise forms.ValidationError("Datum »od« mora biti pred datumom »do«.")
        return podatki

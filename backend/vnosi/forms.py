from django import forms

from treningi.models import Trening


class ObrokForm(forms.Form):
    opis = forms.CharField(label="Kaj sem jedel", max_length=200)
    kcal = forms.IntegerField(label="Ocena kalorij (kcal)", min_value=1)


class CiljForm(forms.Form):
    kcal = forms.IntegerField(label="Dnevni cilj kalorij (kcal)", min_value=1, max_value=20000)
    voda_ml = forms.IntegerField(label="Dnevni cilj vode (ml)", min_value=1, max_value=20000)


class PocutjeForm(forms.Form):
    ocena = forms.TypedChoiceField(
        label="Počutje (1 = slabo, 5 = odlično)", choices=[(i, i) for i in range(1, 6)], coerce=int
    )
    trening = forms.ModelChoiceField(
        label="Po treningu", queryset=Trening.objects.none(), required=False, empty_label="– del dneva –"
    )

    def __init__(self, *args, uporabnik, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["trening"].queryset = uporabnik.treningi.order_by("-zacetek")


class TezaForm(forms.Form):
    teza_kg = forms.FloatField(label="Teža (kg)", min_value=1)


class KomentarForm(forms.Form):
    besedilo = forms.CharField(label="Komentar", max_length=500)
    trening = forms.IntegerField(required=False, widget=forms.HiddenInput)
    vnos = forms.IntegerField(required=False, widget=forms.HiddenInput)

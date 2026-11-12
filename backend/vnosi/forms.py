from django import forms


class ObrokForm(forms.Form):
    opis = forms.CharField(label="Kaj sem jedel", max_length=200)
    kcal = forms.IntegerField(label="Ocena kalorij (kcal)", min_value=1)


class CiljForm(forms.Form):
    kcal = forms.IntegerField(label="Dnevni cilj kalorij (kcal)", min_value=1, max_value=20000)
    voda_ml = forms.IntegerField(label="Dnevni cilj vode (ml)", min_value=1, max_value=20000)

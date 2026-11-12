from django import forms


class ObrokForm(forms.Form):
    opis = forms.CharField(label="Kaj sem jedel", max_length=200)
    kcal = forms.IntegerField(label="Ocena kalorij (kcal)", min_value=1)

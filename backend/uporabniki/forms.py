from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField

from .models import Uporabnik


class PrijavaForm(AuthenticationForm):
    username = UsernameField(label="Uporabniško ime ali e-pošta", widget=forms.TextInput(attrs={"autofocus": True}))
    error_messages = {
        **AuthenticationForm.error_messages,
        "invalid_login": "Napačni podatki za prijavo",
    }


class RegistracijaForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Uporabnik
        fields = ("ime", "username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if Uporabnik.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Uporabnik s tem e-naslovom že obstaja.")
        return email

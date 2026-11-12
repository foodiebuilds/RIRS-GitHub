from django import forms
from django.contrib.auth.forms import AuthenticationForm


class PrijavaForm(AuthenticationForm):
    username = forms.CharField(label="Uporabniško ime ali e-pošta")
    error_messages = {
        **AuthenticationForm.error_messages,
        "invalid_login": "Napačni podatki za prijavo",
    }

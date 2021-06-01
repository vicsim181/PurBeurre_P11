from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label="Prénom")
    last_name = forms.CharField(max_length=50, label="Nom de famille")

    class Meta():
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        exclude = []


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Veuillez renseigner une adresse email et un mot de passe valide."
        ),
        'inactive': ("Veuillez valider votre compte en cliquant sur le lien reçu par courriel pour vous connecter."),
    }
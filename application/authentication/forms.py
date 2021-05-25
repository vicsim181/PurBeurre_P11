from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, label="Prénom")
    last_name = forms.CharField(max_length=50, label="Nom de famille")

    class Meta():
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        exclude = []

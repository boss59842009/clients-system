from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django import forms


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        label="Номер телефону",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Номер телефону"
        })
    )

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name","phone_number", "password1", "password2")

class PhoneAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Номер телефону",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Номер телефону"
        })
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Пароль"
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        label="Запамʼятати мене"
        )
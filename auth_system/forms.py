import re

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        label="Номер телефону",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "+380..."
        })
    )

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name","phone_number", "password1", "password2")


    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")

        if not phone:
            return phone
        # приклад: тільки цифри + +
        if not re.match(r"^\+?\d{10,15}$", phone):
            raise forms.ValidationError("Невірний формат номеру телефону")
        
        if len(phone) > 13:
            raise forms.ValidationError("Невірний формат номеру телефону")

        return phone


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label="Новий пароль",
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name","phone_number", "is_active")
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+380...",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")

        if not phone:
            return phone
        # приклад: тільки цифри + +
        if not re.match(r"^\+?\d{10,15}$", phone):
            raise forms.ValidationError("Невірний формат номеру телефону")
        
        if len(phone) > 13:
            raise forms.ValidationError("Невірний формат номеру телефону")

        return phone

    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get("password")

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

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
    
    def clean(self):
        phone_number = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if phone_number and password:
            user = CustomUser.objects.filter(
                phone_number=phone_number
            ).first()
            if user and not user.is_active:
                raise forms.ValidationError(
                    "Ваш обліковий запис не активований. Будь ласка зверніться до адміністратора.",
                    code="inactive",
                )

        return super().clean()
    
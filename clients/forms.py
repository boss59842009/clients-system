import re
from django import forms
from .models import ClientModel


class ClientForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = "__all__"
        exclude = ["is_active"]

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Імʼя"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Прізвище"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "+380..." }),
            "tg": forms.TextInput(attrs={"placeholder": "без @"}),
            "birthdate": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d"
            ),
        }
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # Якщо створення нового клієнта
    #     if self.instance.pk is None:
    #         self.fields.pop("is_active")

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
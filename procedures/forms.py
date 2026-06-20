import re
from django import forms
from procedures.models import MasterModel, ProcedureModel


class MasterForm(forms.ModelForm):
    class Meta:
        model = MasterModel
        fields = "__all__"
        exclude = ["is_active"]

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Імʼя"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Прізвище"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "+380..." }),
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

class ProcedureForm(forms.ModelForm):
    class Meta:
        model = ProcedureModel
        fields = "__all__"
        exclude = ["is_active"]

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Назва"}),
            "description": forms.Textarea(attrs={"placeholder": "Опис"}),
            "price": forms.NumberInput(attrs={"placeholder": "Ціна в ₴" }),
            "duration": forms.NumberInput(attrs={"placeholder": "Тривалість в зв" }),
        }

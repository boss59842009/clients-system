from django.utils import timezone
from django import forms

from appointments.models import AppointmentModel


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = AppointmentModel
        fields = ["master", "client", "procedure", "start_at", "status", "comment"]

        widgets = {
            "master": forms.Select(attrs={"class": "form-select"}),
            "client": forms.Select(attrs={"class": "form-select"}),
            "procedure": forms.Select(attrs={"class": "form-select"}),
            "start_at": forms.DateTimeInput(attrs={"type": "datetime-local", "step": 900}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Введіть коментар", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.start_at:
            local_dt = timezone.localtime(self.instance.start_at)
            self.initial["start_at"] = local_dt.strftime("%Y-%m-%dT%H:%M")

    def clean(self):
        cleaned_data = super().clean()

        master = cleaned_data.get("master")
        start_at = cleaned_data.get("start_at")
        procedure = cleaned_data.get("procedure")

        if not all([master, start_at, procedure]):
            return cleaned_data

        end_at = start_at + timezone.timedelta(minutes=procedure.duration)

        qs = AppointmentModel.objects.filter(
            master=master,
            start_at__lt=end_at,
            end_at__gt=start_at,
        )

        # При редагуванні не перевіряємо сам запис
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "У майстра вже є запис на цей час."
            )

        return cleaned_data
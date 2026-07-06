from datetime import timedelta
from random import choices
from tabnanny import verbose

from django.db import models
from clients.models import ClientModel
from procedures.models import ProcedureModel, MasterModel


class AppointmentModel(models.Model):
    STATUS_CHOICES = (
        ("booked", "Заброньовано"),
        ("done", "Виконано"),
        ("canceled", "Відмінено"),
        ("no_show", "Приховано"),
    )

    master = models.ForeignKey(MasterModel, on_delete=models.CASCADE, verbose_name='Майстер')
    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE, verbose_name='Клієнт')
    procedure = models.ForeignKey(ProcedureModel, on_delete=models.CASCADE, verbose_name='Процедура') 

    start_at = models.DateTimeField(verbose_name='Початок')
    end_at = models.DateTimeField(blank=True, null=True, verbose_name='Завершення')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="booked", verbose_name='Статус')

    comment = models.CharField(max_length=256, blank=True, null=True, verbose_name="Коментар")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.start_at and self.procedure:
            self.end_at = self.start_at + timedelta(minutes=self.procedure.duration)

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.client.last_name} - {self.procedure.title} - {self.master.last_name}'

    class Meta:
        verbose_name = 'Запис клієнта'
        verbose_name_plural = 'Записи клієнтів'
        ordering = ('-start_at',)

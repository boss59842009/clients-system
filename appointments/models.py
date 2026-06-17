from datetime import timedelta

from django.db import models
from clients.models import ClientModel
from procedures.models import ProcedureModel, MasterModel


class AppointmentModel(models.Model):
    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE, verbose_name='Клієнт')
    procedure = models.ForeignKey(ProcedureModel, on_delete=models.CASCADE, verbose_name='Процедура')
    master = models.ForeignKey(MasterModel, on_delete=models.CASCADE, verbose_name='Майстер')
    enroll = models.BooleanField(default=True, verbose_name='Записано')
    completed = models.BooleanField(default=False, verbose_name='Виконано')

    start_at = models.DateTimeField(verbose_name='Початок')
    end_at = models.DateTimeField(blank=True, null=True, verbose_name='Завершення')

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

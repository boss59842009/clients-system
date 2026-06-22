from django.db import models

class ProcedureModel(models.Model):
    title = models.CharField(max_length=100, verbose_name='Назва')
    description = models.TextField(verbose_name='Опис')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ціна')
    duration = models.PositiveIntegerField(verbose_name='Тривалість')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.price} - {self.duration}"

    class Meta:
        verbose_name = 'Процедура'
        verbose_name_plural = 'Процедури'
        ordering = ('id',)

class MasterModel(models.Model):
    last_name = models.CharField(max_length=30, verbose_name='Прізвище')
    first_name = models.CharField(max_length=30, verbose_name='Імʼя')
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='Номер телефону')
    is_active = models.BooleanField(default=True, verbose_name='Активний')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.last_name} - {self.first_name}"

    class Meta:
        verbose_name = 'Майстер'
        verbose_name_plural = 'Майстри'
        ordering = ('-created_at',)

class MasterProcedureModel(models.Model):
    master = models.ForeignKey(MasterModel, on_delete=models.CASCADE, related_name="master_procedures")
    procedure = models.ForeignKey(ProcedureModel, on_delete=models.CASCADE, related_name="procedure_masters")

    def __str__(self):
        return f"{self.master.last_name} - {self.procedure.title}"

    class Meta:
        verbose_name = 'МайстерПроцедура'
        unique_together = ("master", "procedure")

class MasterScheduleModel(models.Model):
    master = models.ForeignKey(MasterModel, on_delete=models.CASCADE)

    date = models.DateField(verbose_name='Дата')
    start_time = models.TimeField(verbose_name='Час початку роботи')
    end_time = models.TimeField(verbose_name='Час завершення роботи')

    is_day_off = models.BooleanField(default=False, verbose_name='Вихідний')

    class Meta:
        verbose_name = 'Розклад майстра'
        verbose_name_plural = 'Розклад майстрів'
        ordering = ('-date',)












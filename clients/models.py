from django.db import models

class ClientModel(models.Model):
    GENDER_CHOICES = (
        ('-', '-'),
        ('male', 'Чоловік'),
        ('female', 'Жінка')
    )

    last_name = models.CharField(max_length=30, verbose_name="Прізвище")
    first_name = models.CharField(max_length=30, verbose_name='Імʼя')
    phone_number = models.CharField(max_length=15, unique=True, verbose_name='Номер телефону')
    tg = models.CharField(max_length=32, unique=True, blank=True, null=True, verbose_name='Нікнейм в телеграм')
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, default="-", verbose_name='Стать')
    birthdate = models.DateField(blank=True, null=True, verbose_name='Дата народження')
    is_active = models.BooleanField(default=True, verbose_name='Активний')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.phone_number}'

    class Meta:
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'
        ordering = ('-created_at',)
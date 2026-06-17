from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="Номер телефону:")
    USERNAME_FIELD = "phone_number"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"


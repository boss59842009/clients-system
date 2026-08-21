from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Контактна інформація", {
            "fields": ("phone_number",),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Контактна інформація", {
            "fields": ("phone_number",),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
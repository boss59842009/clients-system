from datetime import date

from django.core.management.base import BaseCommand

from clients.models import ClientModel


class Command(BaseCommand):
    help = "Створення тестових клієнтів"

    def handle(self, *args, **kwargs):
        clients = [
            ClientModel(
                first_name=f"Тест{i}",
                last_name=f"Користувач{i}",
                phone_number=f"+380670000{i:03d}",
                tg=f"test_user_{i}",
                gender="male" if i % 2 == 0 else "female",
                birthdate=date(
                    1990 + (i % 10),
                    (i % 12) + 1,
                    (i % 28) + 1
                ),
                is_active=True,
            )
            for i in range(1, 21)
        ]

        created = ClientModel.objects.bulk_create(
            clients,
            ignore_conflicts=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Створено {len(created)} тестових клієнтів"
            )
        )
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask


class Command(BaseCommand):
    help = "Видалення періодичних задач"

    def handle(self, *args, **options):
        task_names = [
            "Done appointments per day",
            "Clear old appointments",
        ]

        deleted_count, _ = PeriodicTask.objects.filter(
            name__in=task_names,
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted periodic task 'Done appointments per day' successfully!"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted periodic task 'Clear old appointments' successfully!"
            )
        )
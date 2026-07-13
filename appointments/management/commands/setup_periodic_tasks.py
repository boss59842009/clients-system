from django.core.management.base import BaseCommand
from django_celery_beat.models import CrontabSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Створення періодичних задач"

    def handle(self, *args, **options):
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute="00",
            hour="01",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        )

        PeriodicTask.objects.update_or_create(
            name="Done appointments per day",
            defaults={
                "task": "appointments.tasks.done_appointments_per_day",
                "crontab": schedule,
                "enabled": True,
            },
        )

        self.stdout.write(
            self.style.SUCCESS("Periodic tasks created")
        )
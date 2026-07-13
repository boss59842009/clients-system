import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from appointments.models import AppointmentModel

logger = logging.getLogger(__name__)


@shared_task
def done_appointments_per_day():
    yesterday = timezone.localdate() - timedelta(days=1)

    done_count = (
        AppointmentModel.objects.filter(
            start_at__date=yesterday,
            status="booked",
        )
        .update(status="done")
    )

    logger.info(
        "В статус 'Виконано' переведено %s записів за %s",
        done_count,
        yesterday,
    )









# from django_celery_beat.models import CrontabSchedule, PeriodicTask

# schedule, _ = CrontabSchedule.objects.get_or_create(
#     minute="00",
#     hour="01",
#     day_of_week="*",
#     day_of_month="*",
#     month_of_year="*",
# )

# PeriodicTask.objects.create(
#     crontab=schedule,
#     name="Evening task",
#     task="clients.tasks.evening_task",
# )
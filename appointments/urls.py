from django.urls import path

from appointments.views import (
    appointments_api_view,
    appointments_delete_view,
    appointments_update_view,
    calendar_api_view,
    masters_api_view,
    appointments_create_view,
)

urlpatterns = [
    path('calendar/', calendar_api_view, name='calendar'),
    path('update/<int:pk>/', appointments_update_view, name='appointments-update'),
    path('delete/<int:pk>/', appointments_delete_view, name='appointments-delete'),
    path('create/', appointments_create_view, name='appointments-create'),
    # API
    path('calendar/api/masters/', masters_api_view),
    path('api/', appointments_api_view),
]
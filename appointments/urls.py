from django.urls import path

from appointments.views import (
    appointments_api_view,
    appointments_delete_view,
    appointments_update_view,
    calendar_api_view,
    appointments_create_view,
    load_procedures_view,
    appointments_list_view,
)

urlpatterns = [
    path('', appointments_list_view, name='appointments-list'),
    path('calendar/', calendar_api_view, name='appointments-calendar'),
    path('update/<int:pk>/', appointments_update_view, name='appointments-update'),
    path('delete/<int:pk>/', appointments_delete_view, name='appointments-delete'),
    path('create/', appointments_create_view, name='appointments-create'),
    # API
    path('api/', appointments_api_view),
    # appointments/urls.py

    path("load-procedures/", load_procedures_view, name="load-procedures"),
]
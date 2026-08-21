from django.urls import path
from .views import clients_list_view, clients_detail_view, client_create_view, clients_update_view, clients_delete_view, import_clients_view, client_appointment_create

urlpatterns = [
    path('', clients_list_view, name='clients-list'),
    path('<int:pk>/', clients_detail_view, name='clients-detail'),
    path('create/', client_create_view, name='clients-create'),
    path('update/<int:pk>/', clients_update_view, name='clients-update'),
    path('delete/<int:pk>/', clients_delete_view, name='clients-delete'),
    path('import/', import_clients_view, name='import-clients'),
    path("<int:pk>/appointments/create/", client_appointment_create, name="client-appointment-create"),
]
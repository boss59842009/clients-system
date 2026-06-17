from django.urls import path
from .views import clients_list_view, clients_detail_view, clients_update_view, clients_delete_view

urlpatterns = [
    path('', clients_list_view, name='clients-list'),
    path('<int:pk>/', clients_detail_view, name='clients-detail'),
    path('update/<int:pk>/', clients_update_view, name='clients-update'),
    path('delete/<int:pk>/', clients_delete_view, name='clients-delete'),
]
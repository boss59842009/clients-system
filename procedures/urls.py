from django.urls import path
from .views import masters_list_view, master_detail_view, master_create_view, master_update_view, master_delete_view

urlpatterns = [
    path('masters/', masters_list_view, name='masters-list'),
    path('masters/<int:pk>/', master_detail_view, name='master-detail'),
    path('masters/create/', master_create_view, name='master-create'),
    path('masters/update/<int:pk>/', master_update_view, name='master-update'),
    path('masters/delete/<int:pk>/', master_delete_view, name='master-delete'),
]
from django.urls import path

import procedures
from .views import *

urlpatterns = [
    # MASTERS
    path('masters/', masters_list_view, name='masters-list'),
    path('master/<int:pk>/', master_detail_view, name='master-detail'),
    path('master/create/', master_create_view, name='master-create'),
    path('master/update/<int:pk>/', master_update_view, name='master-update'),
    path('master/delete/<int:pk>/', master_delete_view, name='master-delete'),
    # PROCEDURES
    path('procedures/', procedures_list_view, name='procedures-list'),
    path('procedure/<int:pk>/', procedure_detail_view, name='procedure-detail'),
    path('procedure/create/', procedure_create_view, name='procedure-create'),
    path('procedure/update/<int:pk>/', procedure_update_view, name='procedure-update'),
    path('procedure/delete/<int:pk>/', procedure_delete_view, name='procedure-delete'),
]
from django.urls import path
from .views import login_view, logout_view, user_create_view, user_update_view, user_delete_view, users_list_view

urlpatterns = [
    path("", users_list_view, name="users-list"),
    path("create/", user_create_view, name="user-create"),
    path("update/<int:pk>/", user_update_view, name="user-update"),
    path("delete/<int:pk>/", user_delete_view, name="user-delete"),
    # path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
from django.urls import path
from auth_app.views import (
    LoginView,
    LogoutView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    UserListView,
)

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "create/user/",
        UserCreateView.as_view(),
        name="create",
    ),
    path(
        "update/user/<int:pk>/",
        UserUpdateView.as_view(),
        name="update",
    ),
    path(
        "delete/user/",
        UserDeleteView.as_view(),
        name="update",
    ),
    path(
        "list/user/<int:pk>/",
        UserListView.as_view(),
        name="update",
    ),
]

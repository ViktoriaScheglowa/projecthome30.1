from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from user.apps import UserConfig

from .views import (UserCreateAPIView, UserDestroyAPIView, UserListAPIView,
                    UserRetrieveAPIView, UserUpdateAPIView, PayListView)

app_name = UserConfig.name


urlpatterns = ([
    path("", UserListAPIView.as_view(), name="user-list"),
    path("login/", LoginView.as_view(template_name="login.html"), name='login'),
    path("logout/", LogoutView.as_view(next_page=''), name='logout'),
    path("create/", UserCreateAPIView.as_view(), name="user-create"),
    path("<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user-delete"),
    path("pay/", PayListView.as_view(), name="pay"),
])

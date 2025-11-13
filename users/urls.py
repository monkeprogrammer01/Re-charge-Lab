from django.urls import path
from users.views import register, login, profile

urlpatterns = [
    path("register/", register),
    path("login/", login),
    path("profile/", profile)
]
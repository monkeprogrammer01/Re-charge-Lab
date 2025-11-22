from django.urls import path
from users.views import register, login, profile, forgot_password, logout_user

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("profile/", profile, name="profile"),
    path("reset/", forgot_password, name="forgot_password"),
    path("logout/", logout_user, name="logout")
]
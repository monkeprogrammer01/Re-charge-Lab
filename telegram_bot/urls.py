from django.urls import path
from telegram_bot.views import telegram_connect
urlpatterns = [
    path("connect/", telegram_connect, name="telegram_connect")
]
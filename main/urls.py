from django.urls import path
from main.views import index, calendar

urlpatterns = [
    path("", index, name="main"),
    path("calendar/", calendar, name="calendar")

]
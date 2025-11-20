from django.urls import path
from main.views import index, calendar, get_tasks

urlpatterns = [
    path("", index, name="main"),
    path("calendar/", calendar, name="calendar"),
    path("calendar/tasks/", get_tasks, name="get_tasks"),
]

from django.urls import path
from main.views import index, calendar, get_tasks, add_task, delete_task, update_task

urlpatterns = [
    path("", index, name="main"),
    path("calendar/", calendar, name="calendar"),

    path("calendar/tasks/add/", add_task, name="add_task"),
    path("calendar/tasks/", get_tasks, name="get_tasks"),
    path("calendar/tasks/delete/<int:id>/", delete_task, name="delete_task"),
    path("calendar/tasks/update/<int:id>/", update_task, name="update_task")
]

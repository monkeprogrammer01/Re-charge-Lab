from django.shortcuts import render
from django.http import JsonResponse
from main.models import Task
import json
from datetime import datetime

from django.utils.dateparse import parse_datetime
from django.utils import timezone
def index(request):
    return render(request, "main/index.html")

def calendar(request):

    if request.method == "POST":
        data = json.loads(request.body)
        description = data.get("description")
        start_date_str = data.get('start_date')
        due_date_str = data.get('due_date')
        start_date = None
        due_date = None

        if start_date_str:
            start_date = timezone.make_aware(datetime.fromisoformat(start_date_str))

        if due_date_str:
            due_date = timezone.make_aware(datetime.fromisoformat(due_date_str))

        task = Task.objects.create(
            user=request.user,
            description=description,
            start_date=start_date,
            due_date=due_date,
            status="pending"
        )
        return JsonResponse({"message": "Task created", "task_id": task.id})
    return render(request, "main/calendar.html")


def get_tasks(request):
    user = request.user
    date_str = request.GET.get("date")  # "YYYY-MM-DD"

    tasks_qs = Task.objects.filter(user=user, start_date=date_str)
    tasks_list = [
        {
            "id": t.id,
            "description": t.description,
            "due_date": t.due_date.isoformat() if t.due_date else None,
        }
        for t in tasks_qs
    ]
    return JsonResponse({"tasks": tasks_list})
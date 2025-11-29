from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from main.services import AIService
from main.models import Task, Message, ChatSession
import json
from datetime import datetime, date, timedelta
from main.tasks import remind_task
from django.utils.dateparse import parse_datetime
from django.utils import timezone

ai = AIService()


def index(request):
    return render(request, "main/index.html")


def calendar(request):
    return render(request, "main/calendar.html")


def add_task(request):
    data = json.loads(request.body)
    description = data.get("description")
    status = data.get("status")
    start_date_str = data.get('start_date')
    due_date_str = data.get('due_date')

    start_date = datetime.fromisoformat(start_date_str)
    if timezone.is_naive(start_date):
        start_date = timezone.make_aware(start_date)
    due_date = None
    now = timezone.now()
    time_difference = start_date - now

    if time_difference.total_seconds() < 0:
        return JsonResponse({
            "error": "Cannot add tasks to past dates.",
            "details": f"The selected time has already passed."
        }, status=400)

    if time_difference.total_seconds() < 600:  # 10 минут в секундах
        return JsonResponse({
            "error": "Task must be scheduled at least 10 minutes in advance.",
            "details": f"Please select a time at least 10 minutes from now."
        }, status=400)
    delta = start_date - now - timedelta(minutes=10)
    countdown_seconds = max(delta.total_seconds(), 0)

    task = Task.objects.create(
        user=request.user,
        description=description,
        start_date=start_date,
        due_date=due_date,
        status=status
    )

    remind_task.apply_async(args=[task.id], countdown=countdown_seconds)

    return JsonResponse({"message": "Task created", "task_id": task.id})


def get_tasks(request):
    user = request.user
    date_str = request.GET.get("date")  # "YYYY-MM-DD"

    tasks_qs = Task.objects.filter(user=user, start_date__date=date_str)
    tasks_list = [
        {
            "id": t.id,
            "description": t.description,
            "status": t.status,
            "due_date": t.due_date.isoformat() if t.due_date else None,
        }
        for t in tasks_qs
    ]
    return JsonResponse({"tasks": tasks_list})


def update_task(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        new_status = data.get("status")
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not new_status:
        return JsonResponse({"error": "Missing status"}, status=400)

    try:
        task = Task.objects.get(id=id, user=request.user)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task not found"}, status=404)

    task.status = new_status
    task.save()

    return JsonResponse({"success": True, "status": task.status})


@require_POST
def delete_task(request, id):
    task = Task.objects.filter(user=request.user, id=id)
    task.delete()
    return JsonResponse({"message": "Task deleted", "taskId": id})


def send_message(request):
    if request.method == "POST":
        user_id = request.user.id
        data = json.loads(request.body)
        user_message = data["message"]
        session = ChatSession.get_active_session(request.user)
        if not session:
            session = ChatSession.create_new_session(request.user)
        bot_reply = ai.generate_response(user_id, user_message)
        mood, reason, language = ai.extract_mood_and_reason(bot_reply)
        msg = ai.save_message(user=request.user, user_message=user_message,session=session, date=datetime.now(), mood=mood, reason=reason,
                              language=language, bot_response=bot_reply)

        return JsonResponse({
            "user_message": user_message,
            "bot_reply": bot_reply,
            "mood": mood,
            "reason": reason,
            "language": language,
            "timestamp": msg.created_at

        })


def chat_history(request):
    session = ChatSession.objects.filter(user=request.user).get()
    if not session:
        session = ChatSession.objects.create(user=request.user)
    messages = Message.objects.filter(user=request.user, session=session).order_by(
        "created_at")
    data = [{
        "user_text": msg.user_message,
        "bot_response": msg.bot_response,
        "mood": msg.mood,
        "reason": msg.reason,
        "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M")

    }
        for msg in messages
    ]
    print(data)
    return JsonResponse({
        "messages": data
    })

from celery import shared_task
from django.utils import timezone
from tracker.models import DailyBalance
from main.models import Task
import asyncio
import logging
import requests
import os

logger = logging.getLogger(__name__)

def send_message_sync(chat_id, text):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

@shared_task
def remind_task(task_id):
    task = Task.objects.get(id=task_id)
    user = task.user
    if user.is_telegram_confirmed:
        text = f"Quick reminder: {task.description} (10 minutes left)"
        send_message_sync(chat_id=user.telegram_chat_id, text=text)
    task.notified = True
    task.save()

@shared_task
def reminder_meal(meal_type: str):
    today = timezone.localdate()
    balances = DailyBalance.objects.filter(
        **{f"{meal_type}_notified": False, "user__is_telegram_confirmed": True, "date": today}
    )

    for balance in balances:
        if not balance.meals.get(meal_type, False):
            text = f"Don't forget to have your {meal_type}"
            send_message_sync(chat_id=balance.user.telegram_chat_id, text=text)
            setattr(balance, f"{meal_type}_notified", True)
            balance.save()

@shared_task(name="main.tasks.reminder_breakfast")
def reminder_breakfast():
    return reminder_meal("breakfast")

@shared_task(name="main.tasks.reminder_lunch")
def reminder_lunch():
    return reminder_meal("lunch")

@shared_task(name="main.tasks.reminder_dinner")
def reminder_dinner():
    return reminder_meal("dinner")

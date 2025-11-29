from celery import shared_task
from django.utils import timezone
from tracker.models import DailyBalance
from main.models import Task
from telegram_bot.bot import send_message_async, send_message_sync
import asyncio
import logging

logger = logging.getLogger(__name__)

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
    filter_kwargs = {f"meals__{meal_type}": False, "user__is_telegram_confirmed": True, "date": today}
    balances = DailyBalance.objects.filter(**filter_kwargs)
    text = f"Dont forget to have your {meal_type}"
    for balance in balances:
        send_message_sync(balance.user.telegram_chat_id, text)

@shared_task(name="main.tasks.reminder_breakfast")
def reminder_breakfast():
    return reminder_meal("breakfast")

@shared_task
def reminder_lunch():
    return reminder_meal("lunch")

@shared_task
def reminder_dinner():
    return reminder_meal("dinner")

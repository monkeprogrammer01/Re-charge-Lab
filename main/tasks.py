import asyncio

from celery import shared_task
from django.utils import timezone
from main.models import Task
from telegram_bot.bot import send_message_async


@shared_task
def remind_task(task_id):
    task = Task.objects.get(id=task_id)
    user = task.user
    if user.is_telegram_confirmed:
        text = f"Quick reminder: {task.description} (10 minutes left)"
        asyncio.run(send_message_async(user.telegram_chat_id, text))

    task.notified = True
    task.save()
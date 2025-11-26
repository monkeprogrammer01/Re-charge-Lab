from django.contrib import admin

from main.models import Task, ChatSession, Message
admin.site.register(Task)
admin.site.register(ChatSession)
admin.site.register(Message)
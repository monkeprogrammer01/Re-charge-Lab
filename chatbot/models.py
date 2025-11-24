
from django.db import models
from django.utils import timezone

from users.models import User

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_number = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'session_number']
        ordering = ['user', '-created_at']

    @property
    def message_count(self):
        return self.messages.count()

    def end_session(self):
        self.is_active = False
        self.ended_at = timezone.now()
        self.save()

    @classmethod
    def get_active_session(cls, user):
        return cls.objects.filter(user=user, is_active=True).first()

    @classmethod
    def create_new_session(cls, user):
        last_session = cls.objects.filter(user=user).order_by("-session_number").first()
        new_number = last_session.session_number + 1 if last_session else 1

        return cls.objects.create(
            user=user,
            session_number= new_number,
            is_active=True
        )

    def __str__(self):
        return f"Session {self.session_number} - User {self.user.email}"

class Message(models.Model):
    MOOD_CHOICES = [
        ('good', 'Good'),
        ('neutral', 'Neutral'),
        ('bad', 'Bad'),
        ('excellent', 'Excellent'),
        ('depressed', 'Depressed'),
        ('anxious', 'Anxious'),
    ]

    LANGUAGE_CHOICES = [
        ('kz', 'Kazakh'),
        ('ru', 'Russian'),
        ('en', 'English'),
        ('unknown', 'Unknown'),
    ]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    user_message = models.TextField()
    bot_response = models.TextField()
    mood = models.CharField(max_length=12, choices=MOOD_CHOICES, default="neutral")
    language = models.CharField(max_length=16, choices=LANGUAGE_CHOICES, default="unknown")
    reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.user.email} - Session {self.session}"

    class Meta:
        ordering = ['-created_at']
from django.db import models
from users.models import User
from django.utils import timezone

class Challenge(models.Model):

    challenge_topics = (
        ('programming', 'Programming'),
        ('algorithms', 'Algorithms'),
        ('math', 'Math'),
        ('language', 'Language'),
    )

    status_choices = (
        ('active', 'Active'),
        ('failed', 'Failed'),
        ('completed', 'Completed')
    )
    difficulty_choices = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    difficulty = models.CharField(max_length=8, choices=difficulty_choices)
    description = models.TextField()
    topic = models.CharField(max_length=16, choices=challenge_topics)
    status = models.CharField(max_length=16, choices=status_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - {self.created_at}"
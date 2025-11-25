from django.db import models
from users.models import User
from django.utils import timezone


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Challenge(models.Model):
    DIFFICULTY_EASY = "easy"
    DIFFICULTY_MEDIUM = "medium"
    DIFFICULTY_HARD = "hard"

    DIFFICULTY_CHOICES = [
        (DIFFICULTY_EASY, "Easy"),
        (DIFFICULTY_MEDIUM, "Medium"),
        (DIFFICULTY_HARD, "Hard"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default=DIFFICULTY_EASY,
    )

    # для ИИ-бота: какие челленджи активны сегодня
    is_active = models.BooleanField(default=True)
    available_from = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def points(self) -> int:
        if self.difficulty == self.DIFFICULTY_EASY:
            return 10
        if self.difficulty == self.DIFFICULTY_MEDIUM:
            return 20
        if self.difficulty == self.DIFFICULTY_HARD:
            return 30
        return 0


class ChallengeCompletion(models.Model):
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"

    STATUS_CHOICES = [
        (STATUS_IN_PROGRESS, "In progress"),
        (STATUS_DONE, "Done"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_IN_PROGRESS,
    )
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "challenge")  # один раз на юзера

    def __str__(self):
        return f"{self.user} – {self.challenge} ({self.status})"
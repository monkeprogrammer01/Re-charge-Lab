from django.db import models
from users.views import User
from django.utils import timezone

class DailyBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meals = models.JSONField(default=dict)
    water = models.PositiveIntegerField(default=0)
    movement_minutes = models.PositiveIntegerField(default=0)
    went_outside = models.BooleanField(default=False)
    coffee_cups = models.PositiveIntegerField(default=0)
    sugar = models.PositiveIntegerField(default=0)
    mood = models.TextField(default="Good")
    relaxation_minutes = models.PositiveIntegerField(default=0)
    completed_challenge = models.BooleanField(default=False)
    social_connections = models.JSONField(
        default=list,
    )

    breakfast_notified = models.BooleanField(default=False)
    lunch_notified = models.BooleanField(default=False)
    dinner_notified = models.BooleanField(default=False)

    total_points = models.PositiveIntegerField(default=0)

    def calculate_points(self):
        meal_points = sum(10 for eaten in self.meals.values() if eaten)
        water_points = self.water
        movement_points = (self.movement_minutes / 30)* 20
        relaxation_minutes = (self.relaxation_minutes / 10) * 5
        completed_challenge = 20 if self.completed_challenge else 0
        social_points = len(self.social_connections) * 5
        self.total_points = round(meal_points + water_points + movement_points + relaxation_minutes + completed_challenge + social_points)
        return self.total_points

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']
    def __str__(self):
        return f"{self.user.email} - {self.date}"

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_type = models.TextField()
    is_eaten = models.BooleanField(default=False)
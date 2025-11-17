from django.http import JsonResponse
from django.shortcuts import render
from tracker.models import DailyBalance
import datetime
import json
def tracker(request):
    user = request.user

    if request.method == "GET":
        today = datetime.date.today()
        daily, created = DailyBalance.objects.get_or_create(user=user, date=today)
        print(daily.meals)
        context = {
            "meals": daily.meals,
            "water": daily.water,
            "movement_minutes": daily.movement_minutes,
            "went_outside": daily.went_outside,
            "relaxation_minutes": daily.relaxation_minutes,
            "social_connections": daily.social_connections,
            "completed_challenge": daily.completed_challenge,
            "total_points": daily.total_points
        }
        return render(request, "tracker/tracker.html", context=context)
    if request.method == "POST":
        today = datetime.date.today()
        daily, created = DailyBalance.objects.get_or_create(user=user, date=today)
        data = json.loads(request.body)
        field = data.get("field")
        value = data.get("value")
        if field == "meals":
            daily.meals = value
        if field == "water":
            daily.water = value
        daily.save()

        return JsonResponse({"total_points": daily.total_points, "meals": daily.meals})

    return render(request, "tracker/tracker.html")

def rating(request):
    return render(request, "tracker/rating.html")

def challenges(request):
    return render(request, "tracker/challenges.html")
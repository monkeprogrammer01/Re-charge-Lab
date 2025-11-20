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
            "water_range": range(1,11),
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
        field_map = {
            "meals": lambda d, v: setattr(d, "meals", v),
            "water": lambda d, v: setattr(d, "water", v),
            "movement_minutes": lambda d, v: setattr(d, "movement_minutes", v),
            "went_outside": lambda d, v: setattr(d, "went_outside", v),
            "relaxation_minutes": lambda d, v: setattr(d, "relaxation_minutes", v),
            "social_connections": lambda d, v: setattr(d, "social_connections", v),
            "completed_challenge": lambda d, v: setattr(d, "completed_challenge", v),
        }

        handler = field_map.get(field)
        if handler:
            handler(daily, value)
            daily.calculate_points()
            daily.save()

        return JsonResponse({"total_points": daily.total_points, "meals": daily.meals})

    return render(request, "tracker/tracker.html")

def rating(request):
    return render(request, "tracker/rating.html")

def challenges(request):
    return render(request, "tracker/challenges.html")
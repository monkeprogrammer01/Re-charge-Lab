from django.urls import path
from tracker.views import tracker, rating, challenges

urlpatterns = [
    path("", tracker, name="tracker"),
    path("rating/", rating, name="rating"),
    path("challenges/", challenges, name="challenges")
]
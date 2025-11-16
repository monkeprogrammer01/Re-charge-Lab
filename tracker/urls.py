from django.urls import path
from tracker.views import tracker

urlpatterns = [
    path("", tracker, name="tracker"),

]
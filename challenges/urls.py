from django.urls import path
from challenges.views import challenges

urlpatterns = [

    path("", challenges, name="challenges")
]
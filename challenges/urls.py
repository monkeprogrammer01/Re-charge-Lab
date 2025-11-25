from django.urls import path
from . import views

urlpatterns = [
    # /challenges/  -> главная страница с заданиями
    path("", views.challenges_list, name="challenges"),

    # /challenges/<id>/complete/ -> отметить выполнение
    path("<int:challenge_id>/complete/", views.complete_challenge,
         name="complete_challenge"),
]
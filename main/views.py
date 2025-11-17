from django.shortcuts import render

def index(request):
    return render(request, "main/index.html")

def calendar(request):
    return render(request, "main/calendar.html")
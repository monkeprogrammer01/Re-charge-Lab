from django.shortcuts import render

def tracker(request):
    return render(request, "tracker/tracker.html")
from django.shortcuts import render

from challenges.models import Challenge


def challenges(request):
    current_challenges = Challenge.objects.filter(user=request.user).all()
    context = {
        "challenges": current_challenges
    }
    return render(request, 'challenges/challenges.html', context)
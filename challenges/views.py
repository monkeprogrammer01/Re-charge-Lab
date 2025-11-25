from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Challenge, ChallengeCompletion


@login_required
def challenges_list(request):
    # активные челленджи (сюда потом можно подкинуть логику ИИ-бота)
    challenges = Challenge.objects.filter(is_active=True).order_by(
        "difficulty", "id"
    )

    # какие челленджи уже выполнены этим пользователем
    completions = ChallengeCompletion.objects.filter(
        user=request.user,
        status=ChallengeCompletion.STATUS_DONE,
    ).values_list("challenge_id", flat=True)

    completed_ids = set(completions)

    context = {
        "challenges": challenges,
        "completed_ids": completed_ids,
    }
    return render(request, "challenges/challenges.html", context)
    # ^^^ подставь свой путь к шаблону challenges-страницы


@login_required
def complete_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)

    completion, created = ChallengeCompletion.objects.get_or_create(
        user=request.user,
        challenge=challenge,
        defaults={
            "status": ChallengeCompletion.STATUS_DONE,
            "finished_at": timezone.now(),
        },
    )

    if not created and completion.status != ChallengeCompletion.STATUS_DONE:
        completion.status = ChallengeCompletion.STATUS_DONE
        completion.finished_at = timezone.now()
        completion.save()

    return redirect("challenges")  # назад на список челленджей
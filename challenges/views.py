from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import json
from .models import Challenge, ChallengeCompletion


@login_required
def challenges_list(request):
    challenges = Challenge.objects.filter(is_active=True).order_by(
        "difficulty", "id"
    )

    completions = ChallengeCompletion.objects.filter(
        user=request.user,
        status=ChallengeCompletion.STATUS_DONE,
    ).values_list("challenge_id", flat=True)

    completed_ids = set(completions)
    print(completed_ids)
    context = {
        "challenges": challenges,
        "completed_ids": completed_ids,
    }
    return render(request, "challenges/challenges.html", context)



@login_required
def complete_challenge(request, challenge_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    body = json.loads(request.body.decode("utf-8"))
    new_status = body.get("status")

    challenge = get_object_or_404(Challenge, id=challenge_id)

    completion, _ = ChallengeCompletion.objects.get_or_create(
        user=request.user,
        challenge=challenge,
    )

    completion.status = new_status
    if new_status == ChallengeCompletion.STATUS_DONE:
        completion.finished_at = timezone.now()
    completion.save()

    return JsonResponse({"ok": True, "new_status": new_status})
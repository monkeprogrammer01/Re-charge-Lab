from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.db.models import (
    Count, Sum, Case, When, IntegerField, F, Q,
)
from django.shortcuts import render

from challenges.models import Challenge, ChallengeCompletion


@login_required
def rating_view(request):
    # Берём только выполненные челленджи
    base_qs = ChallengeCompletion.objects.filter(
        status=ChallengeCompletion.STATUS_DONE
    ).select_related("user", "challenge")

    # Группируем по пользователю и считаем статистику агрегатами
    agg = (
        base_qs
        .values(
            "user__id",
            "user__email",
            "user__name",
            "user__surname",
        )
        .annotate(
            # общее количество выполненных
            completed=Count("id"),

            # сколько easy/medium/hard
            easy=Count(
                Case(
                    When(challenge__difficulty=Challenge.DIFFICULTY_EASY, then=1),
                    output_field=IntegerField(),
                )
            ),
            medium=Count(
                Case(
                    When(challenge__difficulty=Challenge.DIFFICULTY_MEDIUM, then=1),
                    output_field=IntegerField(),
                )
            ),
            hard=Count(
                Case(
                    When(challenge__difficulty=Challenge.DIFFICULTY_HARD, then=1),
                    output_field=IntegerField(),
                )
            ),

            # сумма поинтов
            total_points=Sum(
                Case(
                    When(
                        challenge__difficulty=Challenge.DIFFICULTY_EASY,
                        then=10,
                    ),
                    When(
                        challenge__difficulty=Challenge.DIFFICULTY_MEDIUM,
                        then=20,
                    ),
                    When(
                        challenge__difficulty=Challenge.DIFFICULTY_HARD,
                        then=30,
                    ),
                    default=0,
                    output_field=IntegerField(),
                )
            ),
        )
        .order_by("-total_points", "user__email")
    )

    leaderboard = []
    you_summary = None

    for idx, row in enumerate(agg, start=1):
        full_name = f"{row['user__name']} {row['user__surname']}".strip()
        display_name = full_name or row["user__email"]

        entry = {
            "rank": idx,
            "user_id": row["user__id"],
            "name": display_name,
            "total_points": row["total_points"] or 0,
            "completed": row["completed"],
            "easy": row["easy"],
            "medium": row["medium"],
            "hard": row["hard"],
        }

        if request.user.id == row["user__id"]:
            you_summary = entry

        leaderboard.append(entry)

    context = {
        "leaderboard": leaderboard,
        "you": you_summary,
    }
    return render(request, "rating/rating.html", context)
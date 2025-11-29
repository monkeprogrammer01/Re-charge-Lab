from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout

from users.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        gender = request.POST.get('gender')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists.')
            return redirect('register')
        user = User.objects.create_user(name=name, surname=surname, email=email, gender=gender, password=password)
        messages.success(request, 'User created successfully!')
        return redirect('login')
    return render(request, 'users/create_account.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user:
            auth_login(request, user)
            token = user.token
            messages.success(request, f"JWT Token: {token}")
            return redirect('profile')
        messages.error(request, "Invalid email or password.")
        return render(request, 'users/sign_in.html')
    return render(request, 'users/sign_in.html')





@login_required
def profile(request):
    from tracker.models import DailyBalance
    from main.models import Task
    user = request.user
    today = timezone.localdate()
    now = timezone.now()

    try:

        today_tasks = Task.objects.filter(
            user=user,
            start_date__date=today
        ).order_by('start_date')
        completed_tasks = today_tasks.filter(is_completed=True).count()
        total_tasks = today_tasks.count()
        upcoming_tasks_count = today_tasks.filter(
            is_completed=False,
            start_date__gt=now
        ).count()

        week_ago = today - timedelta(days=7)
        weekly_completed = Task.objects.filter(
            user=user,
            is_completed=True,
            start_date__date__gte=week_ago
        ).count()

        today_stats = DailyBalance.objects.filter(user=user, date=today).first()
        meals = today_stats.meals if today_stats else {}

        streak_days = calculate_streak(user)

        breakfast_progress = 100 if meals.get('breakfast') else 0
        lunch_progress = 100 if meals.get('lunch') else 0
        dinner_progress = 100 if meals.get('dinner') else 0
        water_progress = min((today_stats.water or 0) * 20, 100) if today_stats else 0

        context = {
            'user': user,
            'today_tasks': today_tasks,
            'completed_tasks': completed_tasks,
            'total_tasks': total_tasks,
            'upcoming_tasks_count': upcoming_tasks_count,
            'weekly_completed': weekly_completed,
            'streak_days': streak_days,
            'breakfast_progress': breakfast_progress,
            'lunch_progress': lunch_progress,
            'dinner_progress': dinner_progress,
            'water_progress': water_progress,
        }

        return render(request, 'users/profile.html', context)

    except Exception as e:
        print(e)
        # Fallback context если что-то пойдет не так
        context = {
            'user': user,
            'today_tasks': [],
            'completed_tasks': 0,
            'total_tasks': 0,
            'upcoming_tasks_count': 0,
            'weekly_completed': 0,
            'streak_days': 0,
            'breakfast_progress': 0,
            'lunch_progress': 0,
            'dinner_progress': 0,
            'water_progress': 0,
        }
        return render(request, 'users/profile.html', context)


def calculate_streak(user):
    from tracker.models import DailyBalance
    from main.models import Task
    try:
        today = timezone.localdate()
        streak = 0

        for days_ago in range(30):
            check_date = today - timedelta(days=days_ago)

            has_completed_tasks = Task.objects.filter(
                user=user,
                start_date__date=check_date,
                completed=True
            ).exists()

            has_any_activity = Task.objects.filter(
                user=user,
                start_date__date=check_date
            ).exists() or DailyBalance.objects.filter(
                user=user,
                date=check_date
            ).exists()

            if has_completed_tasks:
                streak += 1
            elif has_any_activity:
                break
            else:
                continue

        return streak
    except:
        return 0
def forgot_password(request):
    return render(request, 'users/forgot_pass.html')

def logout_user(request):
    logout(request)
    return redirect('auth/login/')
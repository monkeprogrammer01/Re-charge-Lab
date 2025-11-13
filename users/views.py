from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from users.models import User

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists.')
            return redirect('register')
        user = User.objects.create_user(email=email, password=password)
        messages.success(request, 'User created successfully!')
        return redirect('login')
    return render(request, 'users/register.html')

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
        return redirect("auth/login")
    return render(request, 'users/login.html')


def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})



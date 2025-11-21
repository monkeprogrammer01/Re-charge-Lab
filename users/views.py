from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from users.models import User

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


def profile(request):
    return render(request, 'users/profile.html')


def forgot_password(request):
    return render(request, 'users/forgot_pass.html')
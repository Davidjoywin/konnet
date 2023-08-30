from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import tokens
from django.contrib.auth import login, logout, authenticate

from .models import Profile


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email=request.POST.get("email")
        username=request.POST.get("username").lower()
        password1=request.POST.get("password1")
        password2=request.POST.get("verify-password")

        password_confirmed = password1 == password2

        if password_confirmed:
            password = make_password(password1)
        else:
            messages.info(request, "Confirmation password incorrect!")
            return redirect('auth:register')
        
        profile = Profile.objects.create(
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            email = email
        )
        profile.save()

        login(request, profile)
        return redirect('post:home')
    return render(request, 'auth/register.html')

def auth_login(request):
    if request.method == 'POST':
        username=request.POST.get("username").lower()
        password=request.POST.get("password")
        
        user=authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("post:home")
        else:
            messages.add_message(request, messages.ERROR, "Username or Password incorrect!")
    return render(request, "auth/login.html")

def auth_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("auth:login")
    return redirect("auth:login")

def page_not_found(request, exception):
    return render(request, 'error/404.html')

def server_error(request, *args, **kwargs):
    return render(request, 'error/500.html')
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import tokens
from django.contrib.auth import login, logout, authenticate


def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('fname')
        email=request.POST.get("email")
        username=request.POST.get("username").lower()
        password1=request.POST.get("password")
        password2=request.POST.get("verify-password")

        first_name, last_name = full_name.split(' ') if len(full_name.split(' ')) == 2 else [full_name, None]

        verified = password1 == password2

        if verified:
            password = make_password(password1)
        else:
            messages.info(request, "Confirmation password incorrect!")
            return redirect('auth:register')
        
        user = User.objects.create(
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            email = email
        )
        user.save()

        login(request, user)
        return redirect('post:home')  
    return render(request, 'auth/signup.html')

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
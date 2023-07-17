from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import tokens
from django.contrib.auth import login, logout, authenticate

def index(request):
    return redirect("chat:home")

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('fname')
        email=request.POST.get("email")
        username=request.POST.get("username")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")

        first_name, last_name = full_name.split(' ')

        if password1 == password2:
            password = make_password(password1)
            try:
                user=User.objects.create(
                    first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                
                login(request, username=username, password=password)
                user.save()
                # acct = AccountActivationTokenGenerator()
                # acc_token = acct.make_token(user)

                
                # user.email_user(
                #     subject="Account verification", 
                #     message=verify_mail(user.username, acc_token), 
                #     from_email="davidjoy.win@gmail.com"
                #     )
            except Exception:
                messages.error("An error occurred!")
            return redirect("chat:home")
        else:
            messages.error(request, "confirmation password is not correct!")
            return redirect("auth:register")
    else:
        return render(request, 'auth/signup.html')
    
# def activation_prompt(request):
#     return render(request, 'auth/activation_prompt.html')

def auth_login(request):
    if request.method == 'POST':
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("chat:home")
        # return redirect("auth:not-active")
    return render(request, "auth/login.html")

# def not_active(request):
#     return render(request, "auth/not_active.html")

def auth_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("auth:index")
    return redirect("auth:index")

# def verify(request, user, token):
#     user = User.objects.get(username=user)
#     acct = AccountActivationTokenGenerator()
#     is_activated = acct.check_token(user, token)
#     if is_activated:
#         user.is_active = True
#         user.save()
#     messages.success(request, "Account successfully activated!")
#     return redirect("auth:login")
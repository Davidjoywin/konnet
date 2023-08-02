from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def home(request):

    context = {}
    return render(request, 'post/post.html', context)

def profile(request):
    user_profile = request.user.profile
    
    context = {
        'user_profile': user_profile
    }

    return render(request, 'profile/user-profile.html', context)

@login_required
def friend_profile(request, user):
    profile = User.objects.get(username=user).profile

    context = {
        'profile': profile
    }

    return render(request, 'profile/user-profile.html', context)
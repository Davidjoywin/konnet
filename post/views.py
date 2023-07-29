from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("Post timeline")

def profile(request):
    user_profile = request.user.profile
    
    context = {
        'user_profile': user_profile
    }

    return render(request, 'profile/user-profile.html', context)

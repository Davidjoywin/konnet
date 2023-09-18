import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from account.models import Profile
from .models import Post

@csrf_exempt
@login_required
def home(request):

    posts = Post.objects.all()

    if request.method == 'POST':
        user_profile = Profile.objects.get(username=request.user.username)
        data = json.load(request)

        user_post = data['user_post'].strip()
        
        post = Post.objects.create(poster=user_profile, text=user_post)
        post.save()
        return JsonResponse({'status': 201})
    
    context = {'posts': posts}
    return render(request, 'post/post.html', context)

def updatePost(request):
    posts = Post.objects.all()

    posts = Post.objects.values()
    print(posts)

    context = {
        'posts': posts
    }

    return JsonResponse(context)

def profile(request):
    username = request.user.username

    user_profile = Profile.objects.get(username=username)
    posts = Post.objects.filter(poster=user_profile)
    
    context = {
        'user_profile': user_profile,
        "posts": posts
    }

    return render(request, 'profile/user-profile.html', context)

@login_required
def friend_profile(request, user):
    profile = Profile.objects.get(username=user)
    friend_post = Post.objects.filter(poster=profile)

    context = {
        'profile': profile,
        'friend_post': friend_post
    }

    return render(request, 'profile/user-profile.html', context)
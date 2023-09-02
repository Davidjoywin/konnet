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
        user_post = request.POST.get('post')

        post = Post.objects.create(text=user_post)
        print(post)
        post.save()
        return JsonResponse({"post": post})
    context = {'posts': posts}
    return render(request, 'post/post.html', context)

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
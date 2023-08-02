import json
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import Friend, Profile, ChatGroup, Message

@login_required()
def home_chat(request):
    user = request.user.friend
    
    friend_chat = [
        User.objects.get(id=id[0])
        for id in request.user.message_set.values_list('receiver').distinct()
    ]
    friend_list = user.friend_list.all()

    context = {
        'friends': friend_chat
    }

    return render(request, 'friends/chatted_friends.html', context)

@login_required
def chat_friends(request, profile):
    user = request.user

    print(profile)
    
    friend_profile = User.objects.get(username=profile).profile

    print(type(friend_profile.user))

    messages = Message.objects.filter((Q(sender=user)&
                                       Q(receiver=friend_profile)) |
                                       (Q(sender=friend_profile.user)&
                                       Q(receiver=user.profile))
    )

    if request.method == 'POST':
        text = request.POST.get('msg')
        Friend.send_message(sent_from=user, sent_to=friend_profile, text=text)
        return redirect(reverse('chat:chat_friend', args=(friend_profile, )))

    context = {
        'friend_profile': friend_profile,
        'messages': messages.order_by('sent_at')
    }

    return render(request, 'chats/home.html', context)

@login_required
def friends(request):
    friend = request.user.friend
    friend_list = friend.friend_list.all()
    new_friends = [i
        for i in Friend.objects.all()
        if i in friend_list
    ]

    context = {
        'friends': friend_list,
        'new_friends': new_friends
    }

    return HttpResponse()

    # return render(request, 'friends/list_friends.html', context)

def list_friends(request):
    friend = request.user.friend
    friend_list = friend.friend_list.all()

    context = {
        'friends': friend_list
    }

    return render(request, 'friends/list_friends.html', context)
    

def get_unreads(request):
    user_authenticated = request.user
    unread_messages = Message.objects.filter(receiver=user_authenticated.profile, read=False).count()
    unread = {'unread_messages': unread_messages}

    return JsonResponse(unread)

def get_no_friends(request):
    authenticated = request.user
    user = User.objects.get(username=authenticated)
    
    friend = user.friend
    no_of_friends = friend.friend_list.all().count()
    return JsonResponse({"no_of_friends": no_of_friends})

def get_no_groups(request):
    authenticated = request.user
    user_profile = User.objects.get(username=authenticated).profile
    user_group_chat = user_profile.chatgroup_set.all()
    no_chatgroup = user_group_chat.count()

    return JsonResponse({"no_chatgroup": no_chatgroup})
    

def add_new_friends(request, friend):
    Friend.add_friend(request.user, friend)
    return redirect('/')

def get_groups(requests):
    groups = ChatGroup.list_groups()

    context = {
        'groups': groups
    }

    return JsonResponse(context)


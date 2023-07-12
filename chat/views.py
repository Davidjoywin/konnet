import json
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

from .models import Friend, ChatGroup, Message

def home(request):
    user = request.user.friend
    
    friend_list = user.friend_list.all()

    context = {
        'friends': friend_list
    }

    return render(request, 'chats/home.html', context)

def chat_friends(request, profile):
    user = request.user

    # message = request.POST.get('post')

    # sent_messages = Message.objects.filter(sender=user, receiver=friend).order_by('sent_at')

    # received_messages = Message.objects.filter(sender=friend, receiver=user).order_by('sent_at')

    friend_profile = User.objects.get(username=profile).profile

    messages = Message.objects.filter((Q(sender=user)&
                                       Q(receiver=friend_profile)) |
                                       (Q(sender=friend_profile.user)&
                                       Q(receiver=user.profile))
    )

    if request.method == 'POST':
        text = request.POST.get('text-message')
        msg = Message.objects.create(sender=user, receiver=friend_profile, text=text)
        msg.save()
        # Friend.send_message(user, friend_profile, text)

        return redirect(reverse('chat:chat_friend', args=(friend_profile, )))

    context = {
        'friend_profile': friend_profile,
        'messages': messages.order_by('sent_at')
    }

    return render(request, 'chats/chat.html', context)

def list_friends(request):
    return HttpResponse('')

def get_unreads(request):
    user_authenticated = request.user
    unread_messages = Message.objects.filter(sender=user_authenticated, read=False).count()
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




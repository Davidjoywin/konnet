import json
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from account.models import Profile, Friendship
from chat.models import ChatGroup, Message

@login_required()
def chatFriendList(request):
    """
    List friends chatted with:
    from latest to the oldest
    """
    username = request.user.username
    user_profile= Profile.objects.get(username=username)

    sender_receiver_ids = Message.objects.filter(
        Q(sender=user_profile) |
        Q(receiver=user_profile)
    ).values_list('sender', 'receiver')

    # chat id filtering out the auth user id
    chats = []


    for ids in sender_receiver_ids:
        for chat_id in ids:
            if chat_id != user_profile.id:
                chats.append(Profile.objects.get(id=chat_id))

    chats = set(chats) # remove duplicates with set

    # get list messages latest where the chats profile appears as the sender
    # or the receiver and then sort using sent_at(time) as the key
    
    latest_messages = [
        Message.objects.filter(
            (Q(sender=user_profile)&
            Q(receiver=friend_profile)) |
            (Q(sender=friend_profile)&
            Q(receiver=user_profile)
        )).latest()

        for friend_profile in chats
    ]  # Get message latest where friend_profile is either the sender or the receiver

    chatted_friends = sorted(latest_messages, key=lambda k: k.sent_at)
    
    # chatted_friends = [
    #     Profile.objects.get(id=id[0])
    #     for id in Message.objects.filter(sender=sender).values_list('receiver').distinct()
    # ]

    context = {
        'friends': chatted_friends
    }

    return render(request, 'friends/chatted_friends.html', context)

@login_required
def chatWithFriend(request, profile_username):
    """
    Chat interface to chat friends
    """
    user = request.user
    user_profile = Profile.objects.get(username=user.username)
    # friend_profile = Profile.objects.get(username=profile_username)
    friend_profile = Profile.objects.get(username='david')
    messages = Message.objects.filter(
        (Q(sender=user_profile)&
        Q(receiver=friend_profile)) |
        (Q(sender=friend_profile)&
        Q(receiver=user_profile))
    )
    if request.method == 'POST':
        text = request.POST.get('msg')
        print(request.POST.get('msg'))
        Message.send_message(user_profile, text, friend_profile)
        return redirect(reverse('chat:chat_friend', args=(friend_profile, )))

    context = {
        'friend_profile': friend_profile,
        'messages': messages.order_by('sent_at')
    }

    return render(request, 'chats/home.html', context)

@login_required
def FriendList(request):
    """
    List friends. People who are already friends
    """
    user_profile = Profile.objects.get(username=request.user.username)
    friend_list = user_profile.getAcceptedFriends()
    new_friends = [i
        for i in Friendship.objects.all()
        if i in friend_list
    ]

    context = {
        'friends': friend_list,
        'new_friends': new_friends
    }

    return render(request, 'friends/list_friends.html', context)

# def listFriends(request):
#     user_profile = Profile.objects.get(username=request.user.username)
#     friend_list = user_profile.friends.all()
#     context = {
#         'friends': friend_list
#     }

#     return render(request, 'friends/list_friends.html', context)
    

def getNoUnreads(request):
    user_profile = Profile.obects.get(username=request.user.username)

    unread_messages = Message.objects.filter(
        receiver=user_profile.profile, read=False).count()
    
    unread = {'unread_messages': unread_messages}

    return JsonResponse(unread)

def getNoFriends(request):
    authenticated = request.user
    user_profile = Profile.objects.get(username=authenticated)
    
    no_of_friends = user_profile.friends.all().count()
    return JsonResponse({"no_of_friends": no_of_friends})

def getNoGroups(request):
    authenticated = request.user
    user_profile = Profile.objects.get(username=authenticated)
    user_group_chat = user_profile.chatgroup_set.all()
    no_chatgroup = user_group_chat.count()

    return JsonResponse({"no_chatgroup": no_chatgroup})
    

def addNewFriends(request, friend):
    user_profile = Profile.objects.get(username=request.user.username)
    user_profile.addFriend(friend)
    return redirect('/')

def getGroups(request):
    groups = ChatGroup.list_groups()

    context = {
        'groups': groups
    }

    return JsonResponse(context)

@login_required
def followRequest(request):
    user_profile = Profile.objects.get(username=request.user.username)
    get_all_friend_req = user_profile.getFriendRequests()
    
    context = {
        'friend_request': get_all_friend_req
    }

    return render(request, 'friends/friend_req.html', context)
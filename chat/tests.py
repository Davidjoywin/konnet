from django.test import TestCase

# Create your tests here.
from django.db.models import Q
from django.contrib.auth.models import User
from account.models import Profile
from chat.models import ChatGroup, Message


# david = Profile.objects.get(username='david')
# joy = Profile.objects.get(username='joy')
# jason = Profile.objects.get(username='jason')

# Friend.add_friend(david, jason_profile)
# Friend.send_message(david, jason_profile, "hello jason, How are you?") 
# Friend.send_message(david, jason_profile, "hello joy, How are you doing?")

# sender= Profile.objects.get(username='david')

# sender_receiver_ids = Message.objects.filter(Q(sender=sender)|Q(receiver=sender)).values_list('sender', 'receiver')

# # chat id filtering out the auth user id
# chats = []

# for ids in sender_receiver_ids:
#     for chat_id in ids:
#         if chat_id != sender.id:
#             chats.append(Profile.objects.get(id=chat_id))

# chat = set(chats)
# print(chat)

# chats = [
#     Message.objects.filter((Q(sender=sender) & Q(receiver=profile)) | (Q(sender=profile)&Q(receiver=sender))).latest('sent_at')
#     for profile in chat
# ]

# print(chats)

# chats = [
#     (profile.sender, profile.receiver, str(profile.sent_at)) for profile in chats
# ]

# print(chats)
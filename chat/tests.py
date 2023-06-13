from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from user_auth.models import Profile
from chat.models import Friend, ChatGroup, Message


david = User.objects.get(username='david')
joy = User.objects.get(username='joy')
jason = User.objects.get(username='jason')

david_profile = Profile.objects.get(user=david)
joy_profile = Profile.objects.get(user=joy)
jason_profile = Profile.objects.get(user=jason)

Friend.create_friend(joy)
# Friend.add_friend(david, jason_profile)
# Friend.send_message(david, jason_profile, "hello jason, How are you?") 
# Friend.send_message(david, jason_profile, "hello joy, How are you doing?")

Friend.send_message(joy, david_profile, "I am very fine, sir")

from django.test import TestCase

from .models import Profile, Friendship


david = Profile.objects.get(username='david')
davidjoy = Profile.objects.get(username='davidjoy')
joydavid = Profile.objects.get(username='joydavid')
joy = Profile.objects.get(username='joy')
jason = Profile.objects.get(username='jason')
olivia = Profile.objects.get(username='olivia')


# print(friends)
# print(friend_requests)

# for profile in friends:
#     friendship = Friendship.objects.get(user=david, other_user=profile)
#     print(friendship.accepted)
#     print(friendship)
#     print("===>")
#     if friendship.accepted:
#         profile.friends.add(david)

# Profile.acceptRequest(david, olivia)
# Profile.acceptRequest(david, jason)

profiles = Profile.objects.all()

for profile in profiles:
    print(f"{profile} Friends => {profile.getAcceptedFriends()}")
    print(f"{profile} friends request {profile.getFriendRequests()}")
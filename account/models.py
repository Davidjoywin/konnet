from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import request

class Profile(User):
    cover_image = models.ImageField(upload_to="file/cover", blank=True)
    profile_image = models.ImageField(upload_to="file/profile", blank=True)
    phone_number = models.CharField(max_length=15)
    friends = models.ManyToManyField('Profile', through='Friendship', related_name='friendship')

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.get_username()
    
    def addFriend(self, new_friend):
        if new_friend not in self.friends.all():
            self.friends.add(new_friend)
        elif new_friend in self.getFriendRequests():
            self.acceptRequest(new_friend)

    def removeFriend(self, friend):
        # Remove a friend it does not matter if
        # they are mutual friends already or not
        friendship = Friendship.objects.get(user=self, other_user=friend)
        friendship.delete()

        # set the accepted friendship attribute to False after deleting
        # the friendship where the user is the authenticated
        friendship = Friendship.objects.get(user=friend, other_user=self)
        friendship.accepted = False
        friendship.save()
    
    def getAcceptedFriends(self):
        # Gets friends who are already mutual
        friends = Friendship.objects.filter(user=self, accepted=True)
        return friends

    def getFriendRequests(self):
        # Returns requests to be friends with user
        friends = [
            profile for profile in self.friendship.all()
            if profile not in self.friends.all()
        ]
        return friends
    
    def list_group(self):
        pass

    def acceptRequest(self, other_user):
        friendship = Friendship.objects.create(user=self, other_user=other_user, accepted=True)
        friendship.save()

        friendship = Friendship.objects.get(user=other_user, other_user=self)
        friendship.accepted = True
        friendship.save()

    

class Friendship(models.Model):
    user = models.ForeignKey(Profile, related_name="User", on_delete=models.CASCADE)
    other_user = models.ForeignKey(Profile, related_name="other_user", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    time_request = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_username()} <==> {self.other_user.get_username()}"

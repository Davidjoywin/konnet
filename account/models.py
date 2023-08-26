from django.db import models
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
    
    def getAcceptedFriends(self):
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
    

class Friendship(models.Model):
    user = models.ForeignKey(Profile, related_name="User", on_delete=models.CASCADE)
    other_user = models.ForeignKey(Profile, related_name="other_user", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    time_request = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_username()} => {self.other_user.get_username()}"

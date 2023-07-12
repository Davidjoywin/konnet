from django.db import models
from django.conf import settings

from user_auth.models import Profile
from django.contrib.auth.models import User


class Friend(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    friend_list = models.ManyToManyField(Profile, blank=True)

    class Meta:
        verbose_name='Friend'
        verbose_name_plural = 'Friends'

    def __str__(self):
        return self.user.username
    
    @classmethod
    def list_friends(cls, user):
        return cls.objects.get(user=user).friend_list.all()
    
    @classmethod
    def create_friend(cls, user):
        cls.objects.create(user=user).save()

    @classmethod
    def delete_friend(cls, user):
        cls.objects.get(user=user).delete()
    
    @classmethod
    def send_message(cls, sent_from, sent_to, text):
        sender = cls.objects.get(user=sent_from)
        to = sender.friend_list.get(user=sent_to)
        message = Message.objects.create(sender=sender.user, text=text, receiver=to)
        message.save()

    @classmethod
    def add_friend(cls, user, new_friend):
        user = cls.objects.get(user=user)
        if new_friend.user != user:
            user.friend_list.add(new_friend)

class ChatGroup(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    member = models.ManyToManyField(Profile, blank=True, through='Membership', through_fields=('chat_group', 'profile'))
    
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.name
    
    @classmethod
    def list_groups(cls):
        return cls.objects.all()

    @classmethod
    def create_group(cls, creator, name):
        new_group = cls.objects.create(creator=creator, name=name)
        new_group.save()
        creator_profile = Profile.objects.get(user=creator)
        new_group.member.add(creator_profile)
        #-----------------what i needed to update-----------------
        # chat_group = ChatGroup.objects.get(creator)
        # -------------------------

    #-------correction needed here------------
    #add members to groups
    @classmethod
    def add_group_member(cls, group_name, new_member):
        chat_group = cls.objects.get(name=group_name)
        user_profile = User.objects.get(username=settings.AUTH_USER_MODEL).profile
        auth_user_in_group = chat_group.membership_set.get(profile=user_profile)
        if auth_user_in_group.through.rank == 'Admin':
            chat_group.member.add(new_member)
        else:
            raise PermissionError("Non-admin not allowed to add member")
        #----------------------------


    @classmethod
    def delete_group(cls, name):
        group = cls.objects.get(name=name)
        group.delete()

    def remove_member(self, profile):
        auth_user = self.member.get(user=settings.AUTH_USER_MODEL)

        if auth_user.through.Rank == 'Admin':
            member = self.member.get(user=profile)
            member.remove()
        else:
            raise PermissionError("Non-admin not allowed remove members")
        
    @staticmethod
    def send_message(sender, chat_group, msg):
        
        GroupMessage.objects.create(group=chat_group, text=msg).save()
        
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    text = models.TextField()
    sent_when = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.text[:10]

class Membership(models.Model):
    class Rank(models.TextChoices):
        admin='Admin'
        member='Member'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=8,
        choices=Rank.choices,
        default=Rank.member
        )
    added_when = models.DateTimeField(auto_now=True)
    
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now=True)
    read = models.BooleanField(default=False)
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.text[:10]
    

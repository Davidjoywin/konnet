from django.db import models
from django.conf import settings

from user_auth.models import Profile


class Friend(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    friend_list = models.ManyToManyField(Profile, blank=True)

    class Meta:
        verbose_name='Friends'

    def __str__(self):
        return self.user.username
    
    @classmethod
    def create_friend(cls, user):
        cls.objects.create(user=user).save()
    
    @classmethod
    def send_message(cls, sent_from, sent_to, text):
        sender = cls.objects.get(user=sent_from)
        to = sender.friend_list.get(user=sent_to)
        message = Message.objects.create(sender=sender.user, text=text, receiver=to)
        message.save()

    @classmethod
    def add_friend(cls, user, new_friend):
        user = cls.objects.get(user=user)
        user.friend_list.add(new_friend)

class ChatGroup(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    member = models.ManyToManyField(Profile, blank=True, through='Membership')
    
    class Meta:
        verbose_name = 'Groups'

    def __str__(self):
        return self.name

    @classmethod
    def create_group(cls, creator, name):
        new_group = cls.objects.create(creator=creator, name=name)
        new_group.save()

    @classmethod
    def add_group_member(cls, group_name, new_member):
        group = cls.objects.get(name=group_name)
        auth_user_in_group = group.member.get(user=settings.AUTH_USER_MODEL)
        if auth_user_in_group.through.rank == 'Admin':
            group.member.add(new_member)
        else:
            raise PermissionError("Non-admin not allowed to add member")

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

class Membership(models.Model):
    class Rank(models.TextChoices):
        admin='Admin'
        member='Member'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    chat_group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=8,
        choices=Rank.choices
        )
    added_when = models.DateTimeField(auto_now=True)
    
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now=True)
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Messages'

    def __str__(self):
        return self.text[:10]
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

from .models import Friend


@receiver(post_save, sender=User)
def create_friend(sender, instance, created, **kwargs):
    if created:
        Friend.create_friend(user=instance)

@receiver(post_delete, sender=User)
def delete_friend(sender, instance, **kwargs):
    friend = Friend.objects.get(user=instance)
    friend.delete()
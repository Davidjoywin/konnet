from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
       Profile.create_profile(user=sender)

@receiver(post_delete, sender=User)
def delete_profile(sender, instance, deleted, **kwargs):
    if deleted:
        profile = Profile.objects.get(user=sender)
        profile.delete()
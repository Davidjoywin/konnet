from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
       Profile.create_profile(user=instance)

@receiver(post_delete, sender=User)
def delete_profile(sender, instance, **kwargs):
    try:
        Profile.delete_profile(user=instance)
    except Exception:
        pass

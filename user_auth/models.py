from django.db import models
from django.contrib.auth.models import User
from django.http import request

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cover_image = models.ImageField(upload_to="file/cover", blank=True)
    profile_image = models.ImageField(upload_to="file/profile", blank=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_username()
    
    @classmethod
    def create_profile(cls, user):
        cls.objects.create(user=user).save()


    @classmethod
    def delete_profile(cls, user):
        cls.objects.get(user=user).delete()
    
from django.db import models
from django.conf import settings

from user_auth.models import Profile


class FilePost(models.Model):
    file = models.FileField(upload_to="upload/posts")
    like = models.ManyToManyField(settings.AUTH_USER_MODEL)

class Post(models.Model):
    post_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField()
    file_post = models.ManyToManyField(FilePost)
    when_posted = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.text[:15]
    

class Comment(models.Model):
    post = models.ForeignKey(Post, blank=True, on_delete=models.CASCADE)
    file_post = models.ForeignKey(FilePost, blank=True, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    inner_reply = models.ForeignKey('Reply', on_delete=models.CASCADE)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self):
        return self.text[:10]
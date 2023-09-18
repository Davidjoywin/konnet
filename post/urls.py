from django.urls import path

from . import views


app_name = 'post'
urlpatterns = [
    path('', views.home, name='home'),
    path('update', views.updatePost, name='update-post'),
    path('profile', views.profile, name='profile'),
    path('profile/<str:user>', views.friend_profile, name= "friend-profile"),
]
from django.urls import path

from . import views


app_name = 'post'
urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('', views.timeline, name='timeline')
]
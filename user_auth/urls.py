from django.urls import path

from . import views


app_name = 'auth'
urlpatterns = [
    path('signup', views.register, name='register'),
    path('login', views.auth_login, name='login'),
    path('logout', views.auth_logout, name='logout'),
    path('', views.index, name='index'),
]
from django.urls import path

from . import views


app_name='chat'
urlpatterns = [
    path('', views.home_chat, name='home'),
    path('friends', views.list_friends, name='friends'),
    path('<str:profile>', views.chat_friends, name='chat_friend'),
    path('add-friend/<int:friend>', views.add_new_friends, name='add_friends'),
    path('message/unread', views.get_unreads, name='unreads'),
    path('friends/no', views.get_no_friends, name='no_friends'),
    path('groups/no', views.get_no_groups, name='no_groups'),
]
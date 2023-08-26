from django.urls import path

from . import views
from .models import Profile


app_name='chat'
urlpatterns = [
    path('', views.chatFriendList, name='home'),
    path('friends', views.FriendList, name='friends'),
    path('follow_request', views.followRequest, name='follow-req'),
    path('<str:profile_username>', views.chatWithFriend, name='chat_friend'),
    path('add-friend/<int:friend>', views.addNewFriends, name='add_friends'),
    path('message/unread', views.getNoUnreads, name='unreads'),
    path('friends/no', views.getNoFriends, name='no_friends'),
    path('groups/no', views.getNoGroups, name='no_groups'),
]
from django.urls import path

from . import views


app_name='chat'
urlpatterns = [
    path('', views.chatFriendList, name='home'),
    path('friends', views.acceptedFriends, name='friends'),
    path('follow/request', views.followRequest, name='follow-req'),
    path('<str:friend_username>', views.chatWithFriend, name='chat_friend'),
    path('friend/<str:friend>/add', views.addNewFriends, name='add-friends'),
    path('friend/<str:friend>/accept', views.acceptFriendRequest, name='accept-friend-request'),
    path('friend/<str:friend>/remove', views.removeFriend, name='remove-friend'),
    path('message/unread', views.getNoUnreads, name='unreads'),
    path('friends/no', views.getNoFriends, name='no_friends'),
    path('groups/no', views.getNoGroups, name='no_groups'),
]
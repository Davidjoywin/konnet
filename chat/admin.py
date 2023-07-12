from django.contrib import admin

from .models import Friend, GroupMessage, ChatGroup, Message, Membership


admin.site.register(Friend)
admin.site.register(GroupMessage)
admin.site.register(ChatGroup)
admin.site.register(Message)
admin.site.register(Membership)
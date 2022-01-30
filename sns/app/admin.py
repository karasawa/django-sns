from django.contrib import admin
from .models import Message, Profile, Group, Friend
from django.contrib.auth import get_user_model

admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(Friend)
admin.site.register(get_user_model())

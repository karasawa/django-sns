from django.contrib import admin
from .models import Message
from django.contrib.auth import get_user_model

admin.site.register(Message)
admin.site.register(get_user_model())

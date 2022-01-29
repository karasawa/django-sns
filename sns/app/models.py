from django.db import models
from django.contrib.auth import get_user_model
import uuid

class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    good_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
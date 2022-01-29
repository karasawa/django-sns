from django.db import models
from django.contrib.auth import get_user_model
import uuid

class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=20)
    icon = models.ImageField(null=True, blank=True)
    one_mes = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nick_name


class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    good_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.owner) + '_' + str(self.content)


# class Group(models.Model):
#     id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
#     owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     title = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.title
#
#
# class Friend(models.Model):
#     id = models.UUIDField(default=uuid.uuid4(), primary_key=True)
#     send_from = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     send_to = models.ForeignKey(get_user_model(), related_name=get_user_model(), on_delete=models.CASCADE)
#
#     def __str__(self):
#         return str(self.send_from) + '----->' + str(self.send_to)
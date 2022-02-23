from django.db import models
from django.contrib.auth import get_user_model
import uuid

class Profile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=20)
    icon = models.ImageField(upload_to='../media/images/', default='images/unknown.jpeg', null=True, blank=True)
    one_mes = models.TextField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nick_name


class Group(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,  related_name='group_owner')
    member = models.ManyToManyField(get_user_model(), related_name='group_member')
    title = models.CharField(max_length=30)
    icon = models.ImageField(null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    friend = models.CharField(max_length=30, null=True, blank=True)
    content = models.TextField(max_length=1000)
    good_count = models.PositiveIntegerField(default=0)
    share_count = models.PositiveIntegerField(default=0)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.owner) + '_' + str(self.content)



class Friend(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    send_from = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='friend_send_from')
    send_to = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    profile_send_from = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='profile_send_from')
    profile_send_to = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    deny_flag = models.BooleanField(default=False)
    promise_flag = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.send_from) + '----->' + str(self.send_to)
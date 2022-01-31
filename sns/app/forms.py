from django import forms
from django.contrib.auth import get_user_model
from .models import Profile, Group

class ChatForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label='メッセージ')
    # content = forms.CharField(max_length=100, label='メッセージ')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nick_name', 'one_mes', 'icon']
        labels = {
            'nick_name': 'ニックネーム',
            'icon': '写真',
            'one_mes': 'メッセージ'
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['owner', 'title', 'icon']
        labels = {
            'owner': 'オーナー',
            'title': 'タイトル',
            'icon': '写真'
        }

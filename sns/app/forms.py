from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

class ChatForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label='メッセージ')
    # content = forms.CharField(max_length=100, label='メッセージ')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nick_name', 'icon', 'one_mes']
        labels = {
            'nick_name': 'ニックネーム',
            'icon': '写真',
            'one_mes': 'メッセージ'
        }

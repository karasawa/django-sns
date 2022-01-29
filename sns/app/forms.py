from django import forms
from django.contrib.auth import get_user_model

class ChatForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label='メッセージ')
    # content = forms.CharField(max_length=100, label='メッセージ')
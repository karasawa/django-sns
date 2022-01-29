from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    email = forms.CharField(max_length=25, label='email')
    password = forms.CharField(max_length=20, label='password', widget=forms.PasswordInput())

class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', )
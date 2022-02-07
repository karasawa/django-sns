from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    email = forms.CharField(max_length=25, label='Email')
    password = forms.CharField(max_length=20, label='Password', widget=forms.PasswordInput())

class SignupForm(forms.Form):
    email = forms.EmailField(max_length=25, label='Email')
    password1 = forms.CharField(max_length=20, label='Password1', widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=20, label='Password2', widget=forms.PasswordInput())

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', )
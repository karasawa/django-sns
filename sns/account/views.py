from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as dj_login
from account.forms import LoginForm, SignupForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                dj_login(request, user)
                return redirect('home')
        messages.error(request, 'ログインに失敗しました')
        return render(request, 'page/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'page/login.html', {'form': form})

# class Login(LoginView):
    # form_class = LoginForm
    # template_name = 'page/login.html'

    # def get_context_data(self, **kwargs):
    #     params = super().get_context_data(**kwargs)
    #     params['karasawa'] = 'karasawa'
    #     return params
    #
    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '登録が完了しました')
            return redirect('login')
        messages.error(request, '登録に失敗しました')
        return render(request, 'page/signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'page/signup.html', {'form': form})


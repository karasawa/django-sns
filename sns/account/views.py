from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as dj_login
from account.forms import LoginForm, SignupForm
from django.contrib import messages
from django.contrib.auth import get_user_model
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                dj_login(request, user)
                messages.success(request, 'ようこそ' + str(request.user) + 'さん！')
                return redirect('home')
        messages.error(request, 'ログインに失敗しました')
        return render(request, 'page/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'page/login.html', {'form': form})


def signup(request):
    User = get_user_model()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            if request.POST['password1'] == request.POST['password2']:
                user = User(email=form.cleaned_data['email'])
                user.set_password(form.cleaned_data['password1'])
                user.save()
                messages.success(request, '登録が完了しました')
                return redirect('login')
            messages.error(request, 'パスワードは同じものを入力してください')
            return render(request, 'page/signup.html', {'form': form})
        messages.error(request, '登録に失敗しました')
        return render(request, 'page/signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'page/signup.html', {'form': form})


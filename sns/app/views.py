from django.shortcuts import render, redirect
from .forms import ChatForm, ProfileForm
from .models import Message, Profile
from django.contrib import messages

def home(request):
    return render(request, 'page/home.html', {})


def chat(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        content = request.POST.get('content')
        if form.is_valid():
            Message.objects.create(owner=request.user,
                                   content=content,
                                   )
        mes = Message.objects.all()
        return render(request, 'page/chat.html', {'form': ChatForm(request.POST),
                                                  'mes': mes})
    else:
        mes = Message.objects.all()
        return render(request, 'page/chat.html', {'form': ChatForm(),
                                                  'mes': mes})

def detail(request):
    instance = Profile.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        user = request.user
        nick_name = request.POST.get('nick_name')
        icon = request.POST.get('icon')
        one_mes = request.POST.get('one_mes')
        if form.is_valid():
            if instance:
                instance.update(user=user,
                                nick_name=nick_name,
                                icon=icon,
                                one_mes=one_mes)
                return render(request, 'page/detail.html', {'form': form})
            else:
                Profile.objects.create(user=user,
                                       nick_name=nick_name,
                                       icon=icon,
                                       one_mes=one_mes)
                return render(request, 'page/detail.html', {'form': form})
        else:
            form = ProfileForm()
            messages.error(request, '登録に失敗しました')
            return render(request, 'page/detail.html', {'form': form})
    else:
        if instance:
            data = instance[0]
            form = ProfileForm(initial={'nick_name': data.nick_name,
                                        'icon': data.icon,
                                        'one_mes': data.one_mes})
            return render(request, 'page/detail.html', {'form': form})
        else:
            form = ProfileForm()
            return render(request, 'page/detail.html', {'form': form})
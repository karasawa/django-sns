from django.shortcuts import render, redirect
from .forms import ChatForm, ProfileForm
from .models import Message, Profile, Group, Friend
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

Q(title_startswith='1') | Q(title_endswith='2')

@login_required
def home(request):
    groups = Group.objects.all()
    friends = Friend.objects.filter(promise_flag=True)
    friends = friends.filter(Q(send_from=request.user) | Q(send_to=request.user))
    deny_friends = Friend.objects.filter(deny_flag=False, promise_flag=False)
    deny_friends = deny_friends.filter(Q(send_from=request.user) | Q(send_to=request.user))
    new_chats = Message.objects.all().order_by('-created_at')[:3]
    for i in new_chats:
        print(i.created_at)
    return render(request, 'page/home.html', {'groups': groups,
                                              'friends': friends,
                                              'deny_friends': deny_friends,
                                              'new_chats': new_chats})

@login_required
def group_create(request):
    print('aaa')
    return redirect('home')

@login_required
def friend_delete(request, pk):
    target = Friend.objects.get(id=pk)
    if target:
        target.delete()
        return redirect('home')
    else:
        messages.error(request, '削除に失敗しました')

@login_required
def friend_promise(request, pk):
    target = Friend.objects.get(id=pk)
    if target:
        target.promise_flag = True
        target.save()
        return redirect('home')
    else:
        messages.error(request, '承認に失敗しました')

@login_required
def friend_deny(request, pk):
    target = Friend.objects.get(id=pk)
    if target:
        target.delete()
        return redirect('home')
    else:
        messages.error(request, '申請拒否に失敗しました')

@login_required
def chat(request):
    profile = Profile.objects.filter(user=request.user)
    if request.method == 'POST':
        if profile:
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
            messages.error(request, 'プロフィール情報を登録してから、チャットに参加しましょう')
            return redirect('chat')
    else:
        mes = Message.objects.all()
        return render(request, 'page/chat.html', {'form': ChatForm(),
                                                  'mes': mes})


@login_required
def chat_delete(request):
    # instance = Message.objects.latest('created_at')
    instance = Message.objects.filter(owner=request.user).order_by('-created_at')[0]
    if instance.owner == request.user:
        instance.delete()
        return redirect('chat')
    else:
        messages.error(request, '削除期限が過ぎています')
        return redirect('chat')


@login_required
def profile(request):
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
                messages.success(request, 'プロフィール情報を更新しました')
                return render(request, 'page/profile.html', {'form': form})
            else:
                Profile.objects.create(user=user,
                                       nick_name=nick_name,
                                       icon=icon,
                                       one_mes=one_mes)
                messages.success(request, 'プロフィール情報を登録しました')
                return render(request, 'page/profile.html', {'form': form})
        else:
            form = ProfileForm()
            messages.error(request, '登録に失敗しました')
            return render(request, 'page/profile.html', {'form': form})
    else:
        if instance:
            data = instance[0]
            form = ProfileForm(initial={'nick_name': data.nick_name,
                                        'icon': data.icon,
                                        'one_mes': data.one_mes})
            return render(request, 'page/profile.html', {'form': form})
        else:
            form = ProfileForm()
            return render(request, 'page/profile.html', {'form': form})


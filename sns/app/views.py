from django.shortcuts import render, redirect
from .forms import ChatForm, ProfileForm, GroupForm
from .models import Message, Profile, Group, Friend
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.conf import settings
import os


@login_required
def home(request):
    user = get_user_model().objects.get(email=request.user)
    groups = user.group_member.all()
    friends = Friend.objects.filter(promise_flag=True)
    friends = friends.filter(Q(send_from=request.user) | Q(send_to=request.user))
    deny_friends = Friend.objects.filter(deny_flag=False, promise_flag=False)
    deny_friends = deny_friends.filter(Q(send_from=request.user) | Q(send_to=request.user))
    new_chats = Message.objects.filter(friend=request.user).order_by('-created_at')[:5]
    return render(request, 'page/home.html', {'groups': groups,
                                              'friends': friends,
                                              'deny_friends': deny_friends,
                                              'new_chats': new_chats})

@login_required
def group(request):
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
def friend_search(request):
    promised_friend_list = []
    waiting_approve_list = []
    if request.method == 'POST':
        search = request.POST.get('search')
        if not search:
            return render(request, 'page/friend_search.html', {})
        else:
            users = get_user_model().objects.filter(email__icontains=search)
            for user in users:
                if Friend.objects.filter(promise_flag=True, send_from=request.user, send_to=user.id):
                    promised_friend_list.append(user)
                elif Friend.objects.filter(promise_flag=True, send_from=user.id, send_to=request.user):
                    promised_friend_list.append(user)
                else:
                    if Friend.objects.filter(promise_flag=False, deny_flag=False, send_from=request.user, send_to=user.id):
                        waiting_approve_list.append(user)
                    elif Friend.objects.filter(promise_flag=False, deny_flag=False, send_from=user.id, send_to=request.user):
                        waiting_approve_list.append(user)
                    else:
                        pass
            return render(request, 'page/friend_search.html', {'users': users,
                                                               'search': search,
                                                               'promised_friend_list': promised_friend_list,
                                                               'waiting_approve_list': waiting_approve_list})
    else:
        return render(request, 'page/friend_search.html', {})

@login_required
def friend_request(request, pk):
    instance = get_user_model().objects.get(id=pk)
    user = get_user_model().objects.get(id=pk).email
    user_id = get_user_model().objects.get(id=pk).id
    query1 = Friend.objects.filter(send_from=request.user.id, send_to=user_id)
    query2 = Friend.objects.filter(send_from=user_id, send_to=request.user.id)
    if query1:
        if query1.filter(promise_flag=True):
            messages.error(request, '既に' + user + 'とはフレンドです')
            return redirect('friend_search')
        else:
            messages.error(request, '既に' + user + 'にはフレンド申請済みです')
            return redirect('friend_search')
    elif query2:
        if query2.filter(promise_flag=True):
            messages.error(request, '既に' + user + 'とはフレンドです')
            return redirect('friend_search')
        else:
            messages.error(request, '既に' + user + 'からフレンド申請が来ています')
            return redirect('friend_search')
    else:
        Friend.objects.create(send_from=request.user,
                              send_to=instance,
                              deny_flag=False,
                              promise_flag=False)
        messages.success(request, user + 'へフレンド申請が送信されました')
        return redirect('home')


@login_required
def group_create(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        owner = request.POST.get('owner')
        owner = get_user_model().objects.filter(email__exact=owner)
        title = request.POST.get('title')
        icon = request.POST.get('icon')
        if owner:
            owner = owner[0]
            if form.is_valid:
                Group.objects.create(owner=owner,
                                     title=title,
                                     icon=icon).member.add(owner)
                messages.success(request, title + 'を作成しました')
                form = GroupForm()
                return render(request, 'page/group.html', {'form': form})
            else:
                messages.error(request, 'グループの作成に失敗しました')
                return render(request, 'page/group.html', {'form': form})
        else:
            messages.error(request, 'オーナーには実在するユーザーを入力してください')
            return render(request, 'page/group.html', {'form': form})
    else:
        form = GroupForm()
        return render(request, 'page/group.html', {'form': form})


@login_required
def group_invite(request):
    promised_friend_list = []
    if request.method == 'POST':
        search = request.POST.get('search')
        if not search:
            return render(request, 'page/friend_search.html', {})
        else:
            users = get_user_model().objects.filter(email__icontains=search)
            for user in users:
                if Friend.objects.filter(promise_flag=True, send_from=request.user, send_to=user.id):
                    promised_friend_list.append(user)
                elif Friend.objects.filter(promise_flag=True, send_from=user.id, send_to=request.user):
                    promised_friend_list.append(user)
                else:
                    pass
            return render(request, 'page/friend_search.html', {'users': users,
                                                               'search': search,
                                                               'promised_friend_list': promised_friend_list})
    else:
        return render(request, 'page/friend_search.html', {})


@login_required
def group_invite_request(request, pk):
    group_id = request.session['group_pk']
    instance = get_user_model().objects.get(id=pk)
    user = instance.email
    user_id = instance.id
    group = Group.objects.get(id=group_id)
    query1 = group.member.all()
    if user_id in query1:
        messages.error(request, user + 'は既にグループに参加しています')
        redirect('group_invite')
    else:
        group.member.add(user_id)
        messages.success(request, user + 'を' + group.title + 'に招待しました')
        return redirect('group_invite')


@login_required
def friend_chat(request, pk):
    request.session['friend_pk'] = pk
    user = get_user_model().objects.get(email=request.user)
    friend = Friend.objects.get(id=pk)
    in_speaking_friend = friend
    all_group = user.group_member.all()
    all_friend = Friend.objects.filter(Q(send_from=user.id) | Q(send_to=user.id))
    all_friend = all_friend.filter(promise_flag=True)
    profile = Profile.objects.filter(user=request.user)
    if friend.send_from != request.user:
        friend_profile = Profile.objects.filter(user=friend.send_from)
    else:
        friend_profile = Profile.objects.filter(user=friend.send_to)
    if request.method == 'POST':
        if profile:
            form = ChatForm(request.POST)
            content = request.POST.get('content')
            if form.is_valid():
                Message.objects.create(owner=request.user,
                                       content=content,
                                       friend=friend.id
                                       )
            mes = Message.objects.filter(friend=friend.id)
            return render(request, 'page/chat.html', {'form': ChatForm(request.POST),
                                                      'mes': mes,
                                                      'all_group': all_group,
                                                      'in_speaking_friend': in_speaking_friend,
                                                      'all_friend': all_friend})
        else:
            messages.error(request, 'プロフィール情報を登録してから、チャットに参加しましょう')
            return redirect('friend_chat')
    else:
        mes = Message.objects.filter(friend=friend.id)
        return render(request, 'page/chat.html', {'form': ChatForm(),
                                                  'mes': mes,
                                                  'all_group': all_group,
                                                  'in_speaking_friend': in_speaking_friend,
                                                  'all_friend': all_friend,
                                                  'profile': profile[0],
                                                  'friend_profile': friend_profile[0]})

@login_required
def group_chat(request, pk):
    request.session['group_pk'] = pk
    user = get_user_model().objects.get(email=request.user)
    all_friend = Friend.objects.filter(Q(send_from=user.id) | Q(send_to=user.id))
    all_friend = all_friend.filter(promise_flag=True)
    all_group = user.group_member.all()
    group = Group.objects.get(id=pk)
    in_speaking_group = group
    profile = Profile.objects.filter(user=request.user)
    if request.method == 'POST':
        if profile:
            form = ChatForm(request.POST)
            content = request.POST.get('content')
            if form.is_valid():
                Message.objects.create(owner=request.user,
                                       content=content,
                                       group=group,
                                       )
            mes = Message.objects.filter(group=group)
            return render(request, 'page/chat.html', {'form': ChatForm(request.POST),
                                                      'mes': mes,
                                                      'all_group': all_group,
                                                      'all_friend': all_friend,
                                                      'in_speaking_group': in_speaking_group})
        else:
            messages.error(request, 'プロフィール情報を登録してから、チャットに参加しましょう')
            return redirect('group_chat')
    else:
        mes = Message.objects.filter(group=group)
        return render(request, 'page/chat.html', {'form': ChatForm(),
                                                  'mes': mes,
                                                  'all_group': all_group,
                                                  'all_friend': all_friend,
                                                  'in_speaking_group': in_speaking_group})


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
def friend_chat_delete(request):
    pk = request.session.get('friend_pk')
    friend = Friend.objects.get(id=pk)
    instance = Message.objects.filter(owner=request.user, friend=friend.id).order_by('-created_at')
    if len(instance) == 0:
        messages.error(request, 'あなたのメッセージがありません')
        return redirect('/app/friend_chat/' + pk + '/')
    else:
        if instance[0].owner == request.user:
            instance[0].delete()
            return redirect('/app/friend_chat/' + pk + '/')
        else:
            messages.error(request, '削除期限が過ぎています')
            return redirect('/app/friend_chat/' + pk + '/')


@login_required
def group_chat_delete(request):
    pk = request.session.get('group_pk')
    group = Group.objects.get(id=pk)
    instance = Message.objects.filter(owner=request.user, group=group.id).order_by('-created_at')
    if len(instance) == 0:
        messages.error(request, 'あなたのメッセージがありません')
        return redirect('/app/group_chat/' + pk + '/')
    else:
        if instance[0].owner == request.user:
            instance[0].delete()
            return redirect('/app/group_chat/' + pk + '/')
        else:
            messages.error(request, '削除期限が過ぎています')
            return redirect('/app/group_chat/' + pk + '/')


@login_required
def profile(request):
    instance = Profile.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
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
                instance = Profile.objects.filter(user=request.user)
                url = settings.MEDIA_URL + 'images/' + str(instance[0].icon)
                if os.path.exists(str(url)) is False:
                    url = '/media/images/unknown.jpeg'
                return render(request, 'page/profile.html', {'form': form,
                                                             'url': url})
            else:
                Profile.objects.create(user=user,
                                       nick_name=nick_name,
                                       icon=icon,
                                       one_mes=one_mes)
                instance = Profile.objects.filter(user=request.user)
                url = settings.MEDIA_URL + 'images/' + str(instance[0].icon)
                messages.success(request, 'プロフィール情報を登録しました')
                return render(request, 'page/profile.html', {'form': form,
                                                             'url': url})
        else:
            form = ProfileForm()
            messages.error(request, '登録に失敗しました')
            return render(request, 'page/profile.html', {'form': form,
                                                         'url': '/media/images/unknown.jpeg'})
    else:
        if instance:
            data = instance[0]
            form = ProfileForm(initial={'nick_name': data.nick_name,
                                        'icon': data.icon,
                                        'one_mes': data.one_mes})
            url = settings.MEDIA_URL + 'images/' + str(data.icon)
            if os.path.exists(str(url)) is False:
                url = '/media/images/unknown.jpeg'
            return render(request, 'page/profile.html', {'form': form,
                                                         'url': url})
        else:
            form = ProfileForm()
            return render(request, 'page/profile.html', {'form': form,
                                                         'url': '/media/images/unknown.jpeg'})


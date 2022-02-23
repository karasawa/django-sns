from django.shortcuts import render, redirect
from .forms import ChatForm, ProfileForm, GroupForm
from .models import Message, Profile, Group, Friend
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model


@login_required
def home(request):
    user = get_user_model().objects.get(email=request.user)
    groups = user.group_member.all()
    friends = Friend.objects.filter(promise_flag=True)
    friends = friends.filter(Q(send_from=request.user) | Q(send_to=request.user))
    deny_friends = Friend.objects.filter(deny_flag=False, promise_flag=False)
    deny_friends = deny_friends.filter(Q(send_from=request.user) | Q(send_to=request.user))
    friend_id_list = []
    friend_id_list_send_from = []
    new_chats_list = []
    group_chats_list = []
    new_chats_to_friends = Friend.objects.filter(promise_flag=True, send_from=request.user)
    for new_chats_to_friend in new_chats_to_friends:
        friend_id_list.append(new_chats_to_friend.id)
    new_chats_from_friends = Friend.objects.filter(promise_flag=True, send_to=request.user)
    for new_chats_from_friend in new_chats_from_friends:
        friend_id_list.append(new_chats_from_friend.id)
    new_chats = Message.objects.filter(friend__in=friend_id_list).order_by('-created_at')
    for new_chat in new_chats:
        if new_chat.owner != request.user:
            if new_chat.owner in friend_id_list_send_from:
                pass
            else:
                new_chats_list.append(new_chat)
                friend_id_list_send_from.append(new_chat.owner)
        else:
            pass
    new_chats = new_chats_list[:5]
    for group in groups:
        messages = Message.objects.filter(group=group).order_by('-created_at')
        for message in messages:
            if message.owner == request.user:
                pass
            else:
                group_chats_list.append(message)
                break
    return render(request, 'page/home.html', {'groups': groups,
                                              'friends': friends,
                                              'deny_friends': deny_friends,
                                              'new_chats': new_chats,
                                              'group_chats_list': group_chats_list})

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
    if not Profile.objects.filter(user=request.user):
        messages.error(request, 'はじめに、プロフィールの設定を行ってください')
        return redirect('profile')
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
    user = instance.email
    user_id = instance.id
    query1 = Friend.objects.filter(send_from=request.user.id, send_to=user_id)
    query2 = Friend.objects.filter(send_from=user_id, send_to=request.user.id)
    profile_send_from = Profile.objects.filter(user=request.user.id)[0]
    profile_send_to = Profile.objects.filter(user=user_id)[0]
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
                              promise_flag=False,
                              profile_send_from=profile_send_from,
                              profile_send_to=profile_send_to)
        messages.success(request, user + 'へフレンド申請が送信されました')
        return redirect('home')

@login_required
def group_delete(request, pk):
    target = Group.objects.get(id=pk)
    if target:
        target.delete()
        return redirect('home')
    else:
        messages.error(request, '削除に失敗しました')


@login_required
def group_create(request):
    if not Profile.objects.filter(user=request.user):
        messages.error(request, 'はじめに、プロフィールの設定を行ってください')
        return redirect('profile')
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
                form = GroupForm(request.POST)
                return render(request, 'page/group.html', {'form': form})
            else:
                messages.error(request, 'グループの作成に失敗しました')
                return render(request, 'page/group.html', {'form': form})
        else:
            messages.error(request, 'オーナーには実在するユーザーを入力してください')
            return render(request, 'page/group.html', {'form': form})
    else:
        form = GroupForm()
        user = request.user
        return render(request, 'page/group.html', {'form': form,
                                                   'user': user})


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
        users = get_user_model().objects.all()
        for user in users:
            if Friend.objects.filter(promise_flag=True, send_from=request.user, send_to=user.id):
                promised_friend_list.append(user)
            elif Friend.objects.filter(promise_flag=True, send_from=user.id, send_to=request.user):
                promised_friend_list.append(user)
            else:
                pass
        return render(request, 'page/friend_search.html', {'users': users,
                                                           'promised_friend_list': promised_friend_list})


@login_required
def group_invite_request(request, pk):
    group_id = request.session['group_pk']
    instance = get_user_model().objects.get(id=pk)
    user = instance.email
    user_id = instance.id
    group = Group.objects.get(id=group_id)
    query1 = group.member.all()
    if instance in query1:
        messages.error(request, user + 'は既にグループに参加しています')
        return redirect('group_invite')
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
                                       friend=friend.id,
                                       profile=profile[0]
                                       )
            mes = Message.objects.filter(friend=friend.id)
            return render(request, 'page/chat.html', {'form': ChatForm(request.POST),
                                                      'mes': mes,
                                                      'all_group': all_group,
                                                      'in_speaking_friend': in_speaking_friend,
                                                      'all_friend': all_friend,
                                                      'profile': profile[0],
                                                      'friend_profile': friend_profile[0]})
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
    group_members = group.member.all()
    group_members_list = []
    for group_member in group_members:
        member_profile = Profile.objects.filter(user=group_member.id)[0]
        group_members_list.append(member_profile)
    group_members = group_members_list
    profile = Profile.objects.filter(user=request.user)
    if request.method == 'POST':
        if profile:
            form = ChatForm(request.POST)
            content = request.POST.get('content')
            if form.is_valid():
                Message.objects.create(owner=request.user,
                                       content=content,
                                       group=group,
                                       profile=profile[0]
                                       )
            mes = Message.objects.filter(group=group)
            return render(request, 'page/chat.html', {'form': ChatForm(request.POST),
                                                      'mes': mes,
                                                      'all_group': all_group,
                                                      'all_friend': all_friend,
                                                      'in_speaking_group': in_speaking_group,
                                                      'group_members': group_members})
        else:
            messages.error(request, 'プロフィール情報を登録してから、チャットに参加しましょう')
            return redirect('group_chat')
    else:
        mes = Message.objects.filter(group=group)
        return render(request, 'page/chat.html', {'form': ChatForm(),
                                                  'mes': mes,
                                                  'all_group': all_group,
                                                  'all_friend': all_friend,
                                                  'in_speaking_group': in_speaking_group,
                                                  'group_members': group_members})


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
def friend_chat_delete(request, pk):
    friend_pk = request.session.get('friend_pk')
    message = Message.objects.get(id=pk)
    message.delete()
    return redirect('/app/friend_chat/' + friend_pk + '/')

# @login_required
# def friend_chat_delete(request):
#     pk = request.session.get('friend_pk')
#     friend = Friend.objects.get(id=pk)
#     instance = Message.objects.filter(owner=request.user, friend=friend.id).order_by('-created_at')
#     if len(instance) == 0:
#         messages.error(request, 'あなたのメッセージがありません')
#         return redirect('/app/friend_chat/' + pk + '/')
#     else:
#         if instance[0].owner == request.user:
#             instance[0].delete()
#             return redirect('/app/friend_chat/' + pk + '/')
#         else:
#             messages.error(request, '削除期限が過ぎています')
#             return redirect('/app/friend_chat/' + pk + '/')

@login_required
def group_chat_delete(request, pk):
    group_pk = request.session.get('group_pk')
    message = Message.objects.get(id=pk)
    message.delete()
    return redirect('/app/group_chat/' + group_pk + '/')

# @login_required
# def group_chat_delete(request):
#     pk = request.session.get('group_pk')
#     group = Group.objects.get(id=pk)
#     instance = Message.objects.filter(owner=request.user, group=group.id).order_by('-created_at')
#     if len(instance) == 0:
#         messages.error(request, 'あなたのメッセージがありません')
#         return redirect('/app/group_chat/' + pk + '/')
#     else:
#         if instance[0].owner == request.user:
#             instance[0].delete()
#             return redirect('/app/group_chat/' + pk + '/')
#         else:
#             messages.error(request, '削除期限が過ぎています')
#             return redirect('/app/group_chat/' + pk + '/')


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
                url = icon
                return render(request, 'page/profile.html', {'form': form,
                                                             'url': url})
            else:
                Profile.objects.create(user=user,
                                       nick_name=nick_name,
                                       icon=icon,
                                       one_mes=one_mes)
                url = icon
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
            url = data.icon
            return render(request, 'page/profile.html', {'form': form,
                                                         'url': url})
        else:
            form = ProfileForm()
            return render(request, 'page/profile.html', {'form': form,
                                                         'url': 'unknown.jpeg'})


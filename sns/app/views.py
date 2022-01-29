from django.shortcuts import render, redirect
from .forms import ChatForm
from .models import Message

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
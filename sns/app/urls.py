from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),

    path('chat/', views.chat, name='chat'),
    path('chat_delete/', views.chat_delete, name='chat_delete'),

]

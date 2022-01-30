from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),

    path('chat/', views.chat, name='chat'),
    path('chat_delete/', views.chat_delete, name='chat_delete'),

    path('group_create/', views.group_create, name='group_create'),

    path('friend_delete/<str:pk>/', views.friend_delete, name='friend_delete'),
    path('friend_promise/<str:pk>/', views.friend_promise, name='friend_promise'),
    path('friend_deny/<str:pk>/', views.friend_deny, name='friend_deny'),

]

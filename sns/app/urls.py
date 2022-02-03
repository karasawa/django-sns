from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),

    path('chat/', views.chat, name='chat'),
    path('group_chat/<str:pk>/', views.group_chat, name='group_chat'),
    path('chat_delete/', views.chat_delete, name='chat_delete'),

    path('friend_delete/<str:pk>/', views.friend_delete, name='friend_delete'),
    path('friend_promise/<str:pk>/', views.friend_promise, name='friend_promise'),
    path('friend_deny/<str:pk>/', views.friend_deny, name='friend_deny'),

    path('friend_search/', views.friend_search, name='friend_search'),
    path('friend_request/<str:pk>/', views.friend_request, name='friend_request'),

    path('group_create/', views.group_create, name='group_create'),
    # path('group_invite/', views.group_invite, name='group_invite'),
    path('group/', views.group, name='group'),

]

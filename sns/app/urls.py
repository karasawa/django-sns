from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),

    path('chat/', views.group_chat, name='chat'),
    path('group_chat/<str:pk>/', views.group_chat, name='group_chat'),
    path('friend_chat/<str:pk>/', views.friend_chat, name='friend_chat'),
    path('group_chat_delete/<str:pk>/', views.group_chat_delete, name='group_chat_delete'),
    path('friend_chat_delete/<str:pk>/', views.friend_chat_delete, name='friend_chat_delete'),

    path('friend_delete/<str:pk>/', views.friend_delete, name='friend_delete'),
    path('friend_promise/<str:pk>/', views.friend_promise, name='friend_promise'),
    path('friend_deny/<str:pk>/', views.friend_deny, name='friend_deny'),

    path('friend_search/', views.friend_search, name='friend_search'),
    path('friend_request/<str:pk>/', views.friend_request, name='friend_request'),

    path('group_create/', views.group_create, name='group_create'),
    path('group_delete/<str:pk>/', views.group_delete, name='group_delete'),
    path('group_invite/', views.group_invite, name='group_invite'),
    path('group_invite_request/<str:pk>/', views.group_invite_request, name='group_invite_request'),
    path('group/', views.group, name='group'),

]

from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('detail/', views.detail, name='detail'),

    path('chat/', views.chat, name='chat'),

]

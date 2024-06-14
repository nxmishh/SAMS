from django.urls import path

from . import views

urlpatterns = [
    path("", views.base, name="index"),
    path("login/", views.login, name="login"),
    path("home/", views.home, name="home"),
    path('monitor/', views.monitor, name='monitor'),
    path("logger/", views.logger, name='logger'),
    path("profile/", views.profile, name='profile'),
    path('video_feed/', views.video_feed, name='video_feed'),
]
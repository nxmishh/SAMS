from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.base, name="index"),
    path('login/', auth_views.LoginView.as_view(), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path("home/", views.home, name="home"),
    path('monitor/', views.monitor, name='monitor'),
    path("logger/", views.logger, name='logger'),
    path("profile/", views.profile, name='profile'),    
    path('video_feed/', views.video_feed, name='video_feed'),
    path('fetch-csv/', views.fetch_csv, name='fetch_csv'),
    path('upload/', views.upload_csv, name='upload_csv')
]
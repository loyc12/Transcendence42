#URL configuration
from django.urls import path, include
from core.settings import DJANGO_DEBUG

urlpatterns = [
    path("", include('Home.urls'), name="home"),
    path("login/", include('login.urls')),
    path("users/", include('users.urls')),
    path("game/", include('game.urls')),
    path("tournament/", include('tournament.urls')),
]
#URL configuration
# DOC
# https://docs.djangoproject.com/en/4.2/topics/http/urls/

from django.contrib import admin
from django.urls import path, include
from core.settings import DJANGO_DEBUG

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('Home.urls'), name="home"),
    path("login/", include('login.urls')),
    path("users/", include('users.urls')),
    path("game/", include('game.urls')),
    path("tournament/", include('tournament.urls')),
]
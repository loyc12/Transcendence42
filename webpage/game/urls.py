""" This file contains the URL patterns for the game app. """
from django.urls import path
from . import views

urlpatterns = [
    # URL for the main page (home)
    path("", views.game_home),
    path('join/', views.game_join, name='game_id'),
]

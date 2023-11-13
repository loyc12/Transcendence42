""" This file contains the URL patterns for the game app. """
from django.urls import path
from . import views

urlpatterns = [
    # URL for the main page (home)
    path("", views.game_home),
    path('<int:game_id>', views.create_game, name='game_id')
]

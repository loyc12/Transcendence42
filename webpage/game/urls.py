""" This file contains the URL patterns for the game app. """
from django.urls import path
from . import views, api

urlpatterns = [
    # URL for the main page (home)
    # path("", views.game_home),
    path('join/', views.game_join, name='game_id'),
    path('api/move/w/', api.api_game_press_w),
    path('api/move/s/', api.api_game_press_s),
    path('api/move/a/', api.api_game_press_a),
    path('api/move/d/', api.api_game_press_d),
    path('api/move/up/', api.api_game_press_up),
    path('api/move/down/', api.api_game_press_down),
    path('api/move/left/', api.api_game_press_left),
    path('api/move/right/', api.api_game_press_right),
]

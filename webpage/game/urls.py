""" This file contains the URL patterns for the game app. """
from django.urls import path
from . import views

urlpatterns = [
    # URL for the main page (home)
    path("", views.game_home),
    path('<int:game_id>', views.create_game, name='game_id'),
    #path('redis/set', views.redis_set_test),
    #path('redis/get', views.redis_get_test),
    path('inst_test/create', views.game_create_db_instance),
    path('inst_test/state', views.game_get_state),
    path('inst_test/win', views.game_set_user_as_winner),
    path('inst_test/delete', views.game_delete),
]

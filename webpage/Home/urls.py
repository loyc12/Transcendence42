""" This file contains the URL patterns for the Home app. """
from django.urls import path
from .views import home_view  #logo_view, online_view, profile_view, local_view, hall_view, game_mode_view


urlpatterns = [
#     # URL for the main page (home)
     path("", home_view, name='home' )
#     path('Logo/', logo_view, name='logo' ),
#     path('Hall/', hall_view, name='hall' ),
#     path('Profile/', profile_view, name='profile'),
#     path('Game/', game_mode_view, name='gameMode'),
#     path('Game/', local_view, name='typeLocal'),
#     path('Game/', online_view, name='typeOnline'),
 ]

""" This file contains the URL patterns for the Home app. """
from django.urls import path
from .views import home_view  #logo_view, online_view, profile_view, local_view, hall_view, game_mode_view


urlpatterns = [
#     # URL for the main page (home)
     path("", home_view, name='home' )
 ]

""" This file contains the URL patterns for the Home app. """
from django.urls import path
from .views import home_view, logo_view, profile_view, lobby_main, lobby_view
#from login.views import login_view

urlpatterns = [
    # URL for the main page (home)
    path("", home_view, name='home' ),
    path('Logo/', logo_view, name='logo' ),
    path('Profile/', profile_view, name='profile'),
	path('Visitors/', lobby_main),
	path('Lobby/', lobby_view, name='lobby')
]

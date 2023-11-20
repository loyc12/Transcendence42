""" This file contains the URL patterns for the Home app. """
from django.urls import path
from .views import home_view, logo_view, profile_view
#from login.views import login_view

urlpatterns = [
    # URL for the main page (home)
    path("", home_view, name='home' ),
    path('logo/', logo_view, name='logo'),
    path('profile/', profile_view, name='profile'),
    #path('UserSelect/', selector_view, name='selector' )
]

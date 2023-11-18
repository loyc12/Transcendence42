""" This file contains the URL patterns for the Home app. """
from django.urls import path
from .views import home_view#, logo_view, selector_view
#from login.views import login_view

urlpatterns = [
    # URL for the main page (home)
    path("", home_view, name='home'),
]

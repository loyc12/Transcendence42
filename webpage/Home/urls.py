""" This file contains the URL patterns for the Home app. """
from django.urls import path
from .views import home_view, login_view

urlpatterns = [
    # URL for the main page (home)
    path('home/', home_view, name='home'),
    # URL for the login page
    path('login/', login_view, name='login'),

]

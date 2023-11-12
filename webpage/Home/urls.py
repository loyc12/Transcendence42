""" This file contains the URL patterns for the Home app. """
from django.urls import path
from .views import home_view, login_view

urlpatterns = [
    # URL for the main page (home)
    path("", home_view),
    # URL for the login page (http://127.0.0.1:3000/login/)
    path('index/', login_view, name='index'),

]

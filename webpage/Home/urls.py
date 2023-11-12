""" This file contains the URL patterns for the Home app. """
from django.urls import path
from .views import home_view, login_view, api_view

urlpatterns = [
    # URL for the main page (home)
    path("", home_view),
    path('index/', login_view, name='index'),
    path('login/', api_view, name='42login'),
    # path('api/', api_login, name='api'),
]

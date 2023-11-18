""" This file contains the URL patterns for the Home app. """
from django.urls import path
from .views import home_view, login_view, logo_view, selector_view, shell_view

urlpatterns = [
    # URL for the main page (home)
    path("", home_view, name='home' ),
    # URL for the login page (http://127.0.0.1:3000/login/)
    path('Login/', login_view, name='login'),
    #
    path('Logo/', logo_view, name='logo' ),


    path('Logo/', logo2_view, name='logo2' ),
    #
    path('UserSelect/', selector_view, name='selector' ),

    path('Shell/', shell_view, name='shell' )
]

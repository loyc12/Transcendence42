from django.urls import path
from . import views

urlpatterns = [
    # URL for the main page (home)
    path('Home/', views.home_view, name='home'),
    # URL for the login page
    path('Login/', views.login_view, name='login'),

]

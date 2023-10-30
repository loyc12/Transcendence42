from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_main),
    path('signin/', views.auth_signin),
    path('signup/', views.auth_signup),
    path('signout/', views.auth_signout),
    #path('login/', views.login),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.oauth42),
    path('login/', views.oauth42_login),
    path('callback/', views.oauth42_callback),
    path('receive_code/', views.oauth42_receive_code),
    path('confirm/', views.oauth42_confirm_user)
]
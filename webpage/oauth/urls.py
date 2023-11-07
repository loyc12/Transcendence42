from django.urls import path
from . import views

urlpatterns = [
    path('', views.oauth42),
    path('receive_code/', views.oauth42_receive_code),
    path('confirm/', views.oauth42_confirm_user)
]
from django.urls import path
from . import views

# The `urlpatterns` list routes URLs to views.
urlpatterns = [
    path('profile/get/', views.get_profile)
]
from django.urls import path, include
from . import views

# The `urlpatterns` list routes URLs to views.
urlpatterns = [
    path("delete/", views.user_delete_jimmy)
]
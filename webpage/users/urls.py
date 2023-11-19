from django.urls import path, include
from . import views

# The `urlpatterns` list routes URLs to views.
urlpatterns = [
    path("", views.user_main),
    path("create/", views.user_create),
    path("get/", views.user_get_jimmy),
    path("delete/", views.user_delete_jimmy)
]
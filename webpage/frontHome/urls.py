""" Defines URL patterns for frontHome """
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

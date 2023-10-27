from django.urls import path
from . import views

urlpatterns = [
    path('/', views.),
    path('hello/', views.say_hello_to_my_little_puppy)
]
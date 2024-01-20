from django.urls import path
from . import views

urlpatterns = [
    path('profile/get/', views.get_profile),
    path('profile/logout/', views.force_logout),
]
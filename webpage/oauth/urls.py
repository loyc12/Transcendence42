from django.urls import path
from . import views

urlpatterns = [
    path("", views.oauth42_index, name="index"),
    path("42login/", views.oauth42_login, name="42login"),
    path("42callback/", views.oauth42_callback, name="callback"),
    path("42logout/", views.oauth42_logout, name="42logout"),
    #path("receive_code/", views.oauth42_receive_code),
    #path("confirm/", views.oauth42_confirm_user)
]
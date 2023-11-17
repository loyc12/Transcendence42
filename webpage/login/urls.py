from django.urls import path
from .views import api_view, get_access_token, login_view

urlpatterns = [
    # URL for the main page (home)
    path('', login_view, name='index'),
    path('', api_view, name='42login'),
    path('', get_access_token)
]

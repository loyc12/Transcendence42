from django.urls import path
from .views import api_view, get_access_token

urlpatterns = [
    # URL for the main page (home)
    path('', api_view, name='42login'),
    path('', get_access_token)
]

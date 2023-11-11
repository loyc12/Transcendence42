""" URL Configuration for core app. """
#URL configuration
# DOC
# https://docs.djangoproject.com/en/4.2/topics/http/urls/

from django.contrib import admin
from django.urls import path, include


# The `urlpatterns` list routes URLs to views.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('Home.urls')),
#    path("oauth/", include('oauth.urls')),
    path("users/", include('users.urls'))
]

"""
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
    
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

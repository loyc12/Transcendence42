""" This file is used to render the home page and login page. """
import json
from core.settings import ENV_FILE
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, HttpResponseRedirect#, HttpResponsePermanentRedirect
from django.urls import reverse
#from urllib.parse import urlencode, urlunsplit, quote_plus
#import requests

def login_view(request):
    return render(request, 'Index/index.html')

def home_view(request):
    context = {}
    if not request.user.is_authenticated:
        context['show_login_form'] = True
    return render(request, 'Home/home.html', context)

def api_view(request):
    context = {"session": request.session.get("user"),
               "pretty": json.dumps(request.session.get("user"), indent=4),}
    redirect('https://api.intra.42.fr/oauth/authorize?client_id='+ ENV_FILE['APP42_UID'] + '&redirect_uri=' + ENV_FILE['APP42_OAUTH_REDIRECT'] + '&response_type=code')
    return (HttpResponseRedirect(login_view))

#   &redirect_uri=23.96.3.23:3000/oauth/receive_code

#redirect_uri=23.96.3.23:3000&response_type=code
#&redirect_uri=23.96.3.23:3000/index&response_type=code

# https://docs.djangoproject.com/en/4.2/topics/auth/default/
#keyword :token_generator
# @decorator blabla token
# def api_callback(request):
#     return render(request, 'Home/home.html')

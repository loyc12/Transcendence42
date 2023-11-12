""" This file is used to render the home page and login page. """
import json
from core.settings import ENV_FILE
from django.contrib.auth import authenticate, login
from django.shortcuts import render#, redirect, HttpResponse, HttpResponsePermanentRedirect
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
    return render(request, 'Index/index.html', context)

# def api_login(request):
#     print(request)
#     base_url = "https://api.intra.42.fr/oauth/authorize"
#     params = {
#         "client_id": ENV_FILE['APP42_UID'],
#         "request_uri": ENV_FILE['APP42_OAUTH_REDIRECT']
#     }
#     full_url = urlunsplit(('https', 'api.intra.42.fr', '/oauth/authorize', urlencode(params), None))
#     print("base_url : ", base_url)
#     print("params : ", params)
#     print('full_url : ', full_url)
#     return (HttpResponsePermanentRedirect(requests.build_absolute_uri(full_url)))
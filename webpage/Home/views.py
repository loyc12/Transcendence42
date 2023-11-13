""" This file is used to render the home page and login page. """
import json
from core.settings import ENV_FILE
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect#, HttpResponseRedirect#, HttpResponsePermanentRedirect
from django.urls import reverse_lazy#, reverse
#from urllib.parse import urlencode, urlunsplit, quote_plus
#import requests
#from django.contrib.auth.decorators import permission_required

def login_view(request):
    return render(request, 'Index/index.html')

def home_view(request):
    context = {}
    if not request.user.is_authenticated:
        context['show_login_form'] = True
    return render(request, 'Home/home.html', context)

def api_view(request):
    # Overkill for now, suppose to be the user id code part.
    # context = {"session": request.session.get("user"),
    #            "pretty": json.dumps(request.session.get("user"), indent=4),}

#   Making the url for the api call
    api_url =   ENV_FILE['HTTP_PROTOCOL'] + \
                ENV_FILE['APP42_DOMAIN'] + \
                ENV_FILE['APP42_AUTH'] + \
                '?client_id=' + ENV_FILE['APP42_UID'] + \
                '&redirect_uri=' + ENV_FILE['APP42_OAUTH_REDIRECT'] + \
                '&response_type=code'
                
#   Redirecting to the api call, put the callback url in a variable
    callback = redirect(api_url)
    
#  Return to the callback url, contain a code to get the token
    return (callback)

#Return Code
#http://127.0.0.1:3000/?code=8f05c9296f67d4b1cab461944c0c627672ed12f667d9100c745c9514b991521b

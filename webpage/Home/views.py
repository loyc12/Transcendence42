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

#@permission_required('is_superuser')
def api_view(request):
    # Overkill for now, suppose to be the user id code part.
    # context = {"session": request.session.get("user"),
    #            "pretty": json.dumps(request.session.get("user"), indent=4),}
    
    api_url =   ENV_FILE['HTTP_PROTOCOL'] + \
                ENV_FILE['APP42_DOMAIN'] + \
                ENV_FILE['APP42_AUTH'] + \
                '?client_id=' + ENV_FILE['APP42_UID'] + \
                '&redirect_uri=' + ENV_FILE['APP42_OAUTH_REDIRECT'] + \
                '&response_type=code'
    callback = redirect(api_url)
    return (callback)

#Return Code
#http://127.0.0.1:3000/?code=8f05c9296f67d4b1cab461944c0c627672ed12f667d9100c745c9514b991521b

# https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-060054ee82cdef75be259160866ffaa26f98cef72e59311abfcb9bc609175caf&redirect_uri=http%3A%2F%2F2127.0.0.1%3A3000%2&response_type=code
# https://docs.djangoproject.com/en/4.2/topics/auth/default/
#keyword :token_generator
# @decorator blabla token
# def api_callback(request):
#     return render(request, 'Home/home.html')

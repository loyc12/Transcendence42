""" This file is used to render the home page and login page. """
from django.http import HttpResponse
from core.settings import ENV_FILE
from django.shortcuts import render, redirect
#import requests


def login_view(request):
    return render(request, 'Index/index.html')

def home_view(request):
    context = {}
    if not request.user.is_authenticated:
        context['show_login_form'] = True
    return render(request, 'Home/home.html', context)

def api_view(request):
#   Making the url for the api call
    api_url =   ENV_FILE['HTTP_PROTOCOL'] + \
                ENV_FILE['APP42_DOMAIN'] + \
                ENV_FILE['APP42_AUTH'] + \
                '?client_id=' + ENV_FILE['APP42_UID'] + \
                '&redirect_uri=' + ENV_FILE['APP42_OAUTH_REDIRECT'] + \
                '&response_type=code'
                
#   Redirecting to the api call, put the callback url in a variable
    callback = redirect(api_url)
 #     # Get the code from the callback url
    return (callback)
    #return (get_token(callback))


#POST request to get the token
# def get_token(request):
#     # Get the code from the callback url
#     code = request.GET.get('code')
    
# #   Making the url for the api call
# #   Manque pt code_verifier = https://www.oauth.com/oauth2-servers/access-tokens/authorization-code-request/
#     api_url =   ENV_FILE['HTTP_PROTOCOL'] + \
#                 ENV_FILE['APP42_DOMAIN'] + \
#                 ENV_FILE['APP42_TOKEN'] + \
#                 '?grant_type=authorization_code' + \
#                 '&code=' + code + \
#                 '&redirect_uri=' + ENV_FILE['APP42_OAUTH_REDIRECT'] + \
#                 '&client_id=' + ENV_FILE['APP42_UID'] + \
#                 '&client_secret=' + ENV_FILE['APP42_SECRET']
    
# #   POST request to get the token
#     r = requests.post(api_url)
#     return (HttpResponse(r.text))
#     # access_token = r.json()['access_token']
#     # expires_in = r.json()['expires_in']
#     # if (r.json()['error']):
#     #     endpoint = HttpResponse(".Error from the API.")
#     # else:
#     #     endpoint = HttpResponse(access_token + " " + expires_in)
#     # return (endpoint)
    
    
    
    
    


#Return Code
#http://127.0.0.1:3000/?code=8f05c9296f67d4b1cab461944c0c627672ed12f667d9100c745c9514b991521b

import requests
from django.http import HttpResponseRedirect, HttpResponse
from core.settings import ENV_FILE
from django.shortcuts import render
#import urllib.parse, urllib.request



def login_view(request):
    return render(request, 'Index/index.html')

def home_view(request):
    authorization_code = request.GET.get('code', None)
    if (authorization_code):
        token = get_access_token(authorization_code)
        access_token = requests.post(token)
        return (HttpResponse(access_token))
    return render(request, 'Home/home.html')

def api_view(request):
#   Making the url for the api call
    api_url =   ENV_FILE['HTTP_PROTOCOL'] + \
                ENV_FILE['APP42_DOMAIN'] + \
                ENV_FILE['APP42_AUTH'] + \
                '?client_id=' + ENV_FILE['APP42_UID'] + \
                '&redirect_uri=' + ENV_FILE['APP42_OAUTH_REDIRECT'] + \
                '&response_type=code'
                
#   Redirecting to the api call, put the callback url in a variable
    return (HttpResponseRedirect(api_url))

def get_access_token(autorization_code):
    
    url   = ENV_FILE['HTTP_PROTOCOL'] + \
            ENV_FILE['APP42_DOMAIN'] + \
            ENV_FILE['APP42_TOKEN']
                
    client_id     = ENV_FILE['APP42_UID']
    client_secret = ENV_FILE['APP42_SECRET']
    #redirect_uri  = ENV_FILE['APP42_OAUTH_REDIRECT']
    
    data =  '?grant_type=client_credentials' + \
            '&client_id=' + client_id + \
            '&client_secret=' + client_secret + \
            '&code=' + autorization_code
    return (url + data)
    
    # with urllib.request.urlopen(url, data=data) as response:
    #     token_response = response.read()
    #     return(token_response)

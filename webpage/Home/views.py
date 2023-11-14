import requests
from django.http import HttpResponseRedirect, HttpResponse
from core.settings import ENV_FILE
from django.shortcuts import render
#import urllib.parse, urllib.request

#1352efde99192194de7410129bc9f05c943a78e15490defba18aa95aaa947ed5"

def login_view(request):
    return render(request, 'Index/index.html')

def home_view(request):
    authorization_code = request.GET.get('code', None)
    if (authorization_code):
        token = get_access_token(authorization_code)
        token_code = requests.post(token)
        
        access_token = token_code.json()['access_token']
        
        headers = {'Authorization': 'Bearer ' + access_token}
        url = get_data()
        user_data = requests.get(url, headers=headers)
        return (HttpResponse(user_data.text))
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
    
def get_data():
    url = ENV_FILE['HTTP_PROTOCOL'] + \
          ENV_FILE['APP42_DOMAIN'] + \
          "/v2/users/"
    return (url)
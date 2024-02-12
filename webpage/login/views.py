import requests
from core.settings import ENV_FILE
from django.shortcuts import redirect

#  Create a url will return the access autorisation_code
def api_view(request):
    api_url =   ENV_FILE['HTTP_PROTOCOL'] + \
                ENV_FILE['APP42_DOMAIN'] + \
                ENV_FILE['APP42_AUTH'] + \
                '?client_id=' + ENV_FILE['APP42_UID'] + \
                '&redirect_uri=' + ENV_FILE['APP42_OAUTH_REDIRECT'] + \
                '&response_type=code'
    print("api_view :: api_url : ", api_url)
    return (redirect(api_url))

#  Create a url will return the access token link
def get_access_token(autorization_code):
    url   = ENV_FILE['HTTP_PROTOCOL'] + \
            ENV_FILE['APP42_DOMAIN'] + \
            ENV_FILE['APP42_TOKEN']
                
    client_id     = ENV_FILE['APP42_UID']
    client_secret = ENV_FILE['APP42_SECRET']
    
    data          = '?grant_type=authorization_code' + \
                    '&client_id=' + client_id + \
                    '&client_secret=' + client_secret + \
                    '&code=' + autorization_code + \
                    '&redirect_uri=' + ENV_FILE['APP42_OAUTH_REDIRECT']
            
    return (url + data)
    
#  Create a url will return the public data of the user from the api
def get_api_data():
    url = ENV_FILE['HTTP_PROTOCOL'] + \
          ENV_FILE['APP42_DOMAIN'] + \
          "/v2/me/"
    return (url)
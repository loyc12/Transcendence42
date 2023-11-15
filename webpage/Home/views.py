import requests
from django.http import HttpResponse, HttpResponseRedirect
from core.settings import ENV_FILE
from django.shortcuts import render
from users.views import import_data

#http://127.0.0.1:3000/index/
# Warning : This URL is extra-step,
def login_view(request):
    return render(request, 'Index/index.html')

#http://127.0.0.1:3000/
def home_view(request):
    authorization_code = request.GET.get('code', None)
    if (authorization_code):
        token = get_access_token(authorization_code)
        token_code = requests.post(token)
        access_token = token_code.json()['access_token']
        headers = {'Authorization': 'Bearer ' + access_token}
        url = get_data()
        user_data = requests.get(url, headers=headers)
        import_data(user_data, request)
        return render(request, 'Index/index.html')
    return render(request, 'Home/home.html')

#http://127.0.0.1:3000/login
# Warning : Going to this URL will trigger the oauth2 process
def api_view(request):
    api_url =   ENV_FILE['HTTP_PROTOCOL'] + \
                ENV_FILE['APP42_DOMAIN'] + \
                ENV_FILE['APP42_AUTH'] + \
                '?client_id=' + ENV_FILE['APP42_UID'] + \
                '&redirect_uri=' + ENV_FILE['APP42_OAUTH_REDIRECT'] + \
                '&response_type=code'
    return (HttpResponseRedirect(api_url))

def get_access_token(autorization_code):
    url   = ENV_FILE['HTTP_PROTOCOL'] + \
            ENV_FILE['APP42_DOMAIN'] + \
            ENV_FILE['APP42_TOKEN']
                
    client_id     = ENV_FILE['APP42_UID']
    client_secret = ENV_FILE['APP42_SECRET']
    data =  '?grant_type=authorization_code' + \
            '&client_id=' + client_id + \
            '&client_secret=' + client_secret + \
            '&code=' + autorization_code + \
            '&redirect_uri=' + ENV_FILE['APP42_OAUTH_REDIRECT']
    return (url + data)
    
def get_data():
    url = ENV_FILE['HTTP_PROTOCOL'] + \
          ENV_FILE['APP42_DOMAIN'] + \
          "/v2/me/"
    return (url)
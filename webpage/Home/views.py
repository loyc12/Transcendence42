import requests
from django.http import HttpResponseRedirect, HttpResponse
from core.settings import ENV_FILE
from django.shortcuts import render


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

# "login":"alvachon",
# "displayname":"Alexandra Vachon"

# "image":{"link":"https://cdn.intra.42.fr/users/1a6cf4672ded9069b92b9e7d9a39acb0/alvachon.jpg",
# "versions":{"large":"https://cdn.intra.42.fr/users/c26d9889073d41bdcf67cb0043ed2b6a/large_alvachon.jpg",
# "medium":"https://cdn.intra.42.fr/users/11f8cb615ee7b6d7494be87753c105da/medium_alvachon.jpg",
# "small":"https://cdn.intra.42.fr/users/910efb53059ce3da462a6b86d0b93034/small_alvachon.jpg",
# "micro":"https://cdn.intra.42.fr/users/c36d792fe5c1287dd62b58f15ca4908f/micro_alvachon.jpg"}},

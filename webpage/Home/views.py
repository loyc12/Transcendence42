""" This file is used to render the home page. """
import sys
import requests
# from core.settings import ENV_FILE

from django.contrib.auth import login
from django.shortcuts import render, redirect
from login.views import get_access_token, get_api_data
from users.views import import_data
from users.models import User

def eprint(*args):
    print(*args, file=sys.stderr)

#http://127.0.0.1:3000/
def home_view(request):
    """ This function is used to render the home page. """
    
    eprint('User on Home_View load : ', request.user)
    authorization_code = request.GET.get('code', None)
    if (authorization_code):
        token = get_access_token(authorization_code)
        #This request is to separate the access token from the response
        token_code = requests.post(token, timeout=10)
        access_token = token_code.json()['access_token']
        headers = {'Authorization': 'Bearer ' + access_token}
        url = get_api_data()
        #This request is to get the user data
        user_data = requests.get(url, headers=headers, timeout=10)
        user = import_data(user_data, request)
        login(request, user)
        current_url = request.build_absolute_uri()
        path, _, _ = current_url.partition('?')
        if 'code=' in request.META.get('QUERY_STRING', ''):
            updated_url = path
            request.session['user_id'] = user.id
            request.session['user_login'] = user.login
            request.session.save()
            #This redirect is to remove the code from the url
            return redirect(updated_url)
    
    return render(request, 'master.html')
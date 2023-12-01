""" This file is used to render the home page. """
import requests
# from core.settings import ENV_FILE
from django.contrib.auth import login
from django.shortcuts import render, redirect
from login.views import get_access_token, get_api_data
from users.views import import_data
from users.models import User


#http://127.0.0.1:3000/
def home_view(request):
    """ This function is used to render the home page. """
    authorization_code = request.GET.get('code', None)
    if (authorization_code):
        token = get_access_token(authorization_code)
        token_code = requests.post(token, timeout=10)
        access_token = token_code.json()['access_token']
        headers = {'Authorization': 'Bearer ' + access_token}
        url = get_api_data()
        user_data = requests.get(url, headers=headers, timeout=10)
        user = import_data(user_data, request)
        if user:
            login(request, user)
        current_url = request.build_absolute_uri()
        path, _, _ = current_url.partition('?')
        if 'code=' in request.META.get('QUERY_STRING', ''):
            updated_url = path
            return redirect(updated_url)
        return render(request, 'master.html')
    return render(request, 'master.html')

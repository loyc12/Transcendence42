""" This file is used to render the home page. """
import requests
# from core.settings import ENV_FILE
from django.shortcuts import render
from login.views import get_access_token, get_api_data
from users.views import import_data
#from .forms import ProfileForm


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
        import_data(user_data, request)
        return render(request, 'Home/home.html')
    return render(request, 'Home/home.html')


def logo_view(request):
    """ This function is used to render the logo page. """
    return render(request, 'logo.html')


def profile_view(request):
    """ This function is used to render the profile page. """
    return render(request, 'profile.html')

def game_mode_view(request):
    """ This function is used to render the logo page. """
    return render(request, 'gameMode.html')

def local_view(request):
    """ This function is used to render the logo page. """
    return render(request, 'gameTypeLocal.html')

def online_view(request):
    """ This function is used to render the logo page. """
    return render(request, 'gameTypeOnline.html')
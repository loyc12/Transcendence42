import requests
from core.settings import ENV_FILE
from django.shortcuts import render
from users.views import import_data
from login.views import get_access_token, get_api_data

#http://127.0.0.1:3000/
def home_view(request):
    authorization_code = request.GET.get('code', None)
    if (authorization_code):
        token = get_access_token(authorization_code)
        token_code = requests.post(token)
        access_token = token_code.json()['access_token']
        headers = {'Authorization': 'Bearer ' + access_token}
        url = get_api_data()
        user_data = requests.get(url, headers=headers)
        import_data(user_data, request)
        return render(request, 'Home/home.html')
    return render(request, 'Home/home.html')

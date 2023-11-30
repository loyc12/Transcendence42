from .models import User
from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.http import JsonResponse
import json

# Collect data from API and save it in the database, start session
def import_data(api_data, request):
    
    target_id = api_data.json()['login']
    # Check if user exists and get it
    if (User.objects.filter(login=target_id).exists()):
        User.objects.filter(login=target_id).update(
            is_active = 1,
        )
        u = User.objects.get(login=target_id)

    # If not, create it
    else:
        u = User.objects.create_user(
            login           = target_id,
            display_name    = api_data.json()['displayname'],
            img_link        = api_data.json()['image']['link'],    
            is_active       = 1,    
        )
    # Update session
    u.save()
    request.session['user_id'] = u.login
    request.session['user_login'] = u.login
    request.session.save()
    # session_key = request.session.session_key
    # session = Session.objects.get(session_key=session_key)
    return u

# def remove_data(request):
#     user_id = request.session['user_id']
#     User.objects.filter(id=user_id).update(
#         is_active=0,
#     )
#     request.session.flush()
#     return

def get_profile(request):

    user = request.user

    # payload = {
    #     'display_name': user.display_name,
    #     'login': user.login,
    #     'img': user.img_link,
    #     'is_active': user.is_active,
    #     'is_ingame': user.is_ingame,
    #     'nb_games_played': user.nb_games_played
    # }
    nb_games_played = user.nb_games_played
    is_ingame = user.is_ingame

    return render(request, 'users/profile.html', context={
        'user': request.user,
        'nb_games_played': nb_games_played,
        'is_ingame': is_ingame
        })
    #return JsonResponse(json.loads(payload))
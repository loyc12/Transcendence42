from .models import User
import sys
from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
import json


def eprint(*args):
    print(*args, file=sys.stderr)

def import_data(api_data, request):

    target_id = api_data.json()['login']
    if (User.objects.filter(login=target_id).exists()):
        User.objects.filter(login=target_id).update(
            is_active = 1,
        )
        u = User.objects.get(login=target_id)

    else:
        u = User.objects.create_user(
            login           = target_id,
            display_name    = api_data.json()['displayname'],
            img_link        = api_data.json()['image']['link'],
            is_active       = 1,
        )
    u.save()
    return u

@login_required
def get_profile(request):

    eprint('get_profile :: user is_authenticated : ', request.user.is_authenticated)

    nb_played = request.user.nb_games_played
    nb_officials_played = request.user.nb_official_games_played
    nb_wins = request.user.nb_wins
    nb_given_up = request.user.nb_given_up
    nb_rug_pulled = request.user.nb_rug_pulled
    nb_tournaments_won = request.user.nb_tournaments_won
    nb_losses = request.user.nb_losses

    return render(request, 'users/profile.html', context={
        'user': request.user,
        'nb_played': nb_played,
        'nb_officials_played': nb_officials_played,
        'nb_wins': nb_wins,
        'nb_losses': nb_losses,
        'nb_given_up': nb_given_up,
        'nb_rug_pulled': nb_rug_pulled,
        'nb_tournaments_won': nb_tournaments_won,
        'win_loss_ratio': f'{(request.user.win_loss_ratio):.2%}'#.format(request.user.win_loss_ratio * 100)
        })

def force_logout(request):
    logout(request)
    return JsonResponse({'status': "success"})
from .models import User
from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
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
    return u

@login_required
def get_profile(request):

    # user = request.user

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
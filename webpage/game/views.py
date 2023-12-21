from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render
from game.models import Game, Player, User
from game.forms import GameCreationForm
from game.apps import GameConfig as app
from game.MatchMaker import MatchMakerWarning
from tournament.models import Tournament
import json
import asyncio

# Create your views here.
def game_home(request):
    print(request)
    return render(request, 'game/game_creation_form.html')

def _build_error_payload(msg):
    return {
        'status': 'failure',
        'reason': msg
    }

# @login_required
def game_join(request):
    '''
        The game request process in the frontend should result in
        a json struct sent as body to an endpoint landing on
        the game_join() view.
    '''
    if request.method != 'POST':
        return JsonResponse(_build_error_payload('A request to send a game requires a POST request with a properly formated body.'), status=400)

    print('RECEIVED POST : ', request.POST)
    print('RECEIVED POST BODY : ', request.body)
    jsonform = json.loads(request.body)
    print('jsonform : ', jsonform)
    if not jsonform:
        return JsonResponse(_build_error_payload('Trying to create a game, but either no game creation form was sent or is malformed.'), status=400)

    form = GameCreationForm(jsonform)
    if not form.is_valid():
        return JsonResponse(_build_error_payload('Trying to create a game, but either no game creation form was sent or is missing fields.'), status=400)

    mm = app.get_match_maker()
    print(mm)
    # if lobby_game.is_tournament:
    try:
        lobby_game = mm.join_lobby(request.user, form.cleaned_data)
    except MatchMakerWarning as w:
        return JsonResponse(_build_error_payload(str(w)), status=400)

    if not lobby_game:
        return JsonResponse(_build_error_payload('Joining game lobby failed.'), status=400)

    payload = {
        'status': 'success',
        'sockID': lobby_game.sockID,
        'gameMode': form.cleaned_data['gameMode'],
        'gameType': form.cleaned_data['gameType'],
        'withAI': form.cleaned_data['withAI'] if 'withAI' in form.cleaned_data else False
    }

    ### TODO: CALL GameManager to create game according to request.
    if lobby_game.is_tournament:
        print('game views :: lobby_game is tournament and tourSockID is : ', lobby_game.tourID)
        payload['tourSockID'] = lobby_game.tourID #'Tour_' + payload['sockID']

    return JsonResponse(payload)


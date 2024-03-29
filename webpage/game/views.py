from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from game.forms import GameCreationForm
from game.apps import GameConfig as app
from game.MatchMaker import MatchMakerWarning
from NetworkGateway.NetworkAdaptor import GameGatewayException
import json

def _build_error_payload(msg):
    return {
        'status': 'failure',
        'reason': msg
    }

@login_required
def game_join(request):
    '''
        The game request process in the frontend should result in
        a json struct sent as body to an endpoint landing on
        the game_join() view.
    '''
    if request.method != 'POST':
        return JsonResponse(_build_error_payload('A request to send a game requires a POST request with a properly formated body.'), status=400)

    jsonform = json.loads(request.body)
    if not jsonform:
        return JsonResponse(_build_error_payload('Trying to create a game, but either no game creation form was sent or is malformed.'), status=400)

    form = GameCreationForm(jsonform)
    if not form.is_valid():
        return JsonResponse(_build_error_payload('Trying to create a game, but either no game creation form was sent or is missing fields.'), status=400)

    if form.cleaned_data["gameMode"] == "Tournament":

        gg = app.get_game_gateway()
        try:
            print("\nGame Join :: Try sync check if live tournament exists !!")
            gg.sync_validate_join_tournament_request(request.user)
        except GameGatewayException as e:
            return JsonResponse(_build_error_payload(str(e)), status=400)

    mm = app.get_match_maker()
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

    if lobby_game.is_tournament:
        payload['tourSockID'] = lobby_game.tourID #'Tour_' + payload['sockID']

    return JsonResponse(payload)

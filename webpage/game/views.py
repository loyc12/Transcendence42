from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render 
from game.models import Game, Player, User
from game.forms import GameCreationForm
from game.apps import GameConfig as app
import json

# Create your views here.
def game_home(request):
    print(request)
    return render(request, 'game/game_creation_form.html')
    #return HttpResponse("Welcome to the game home page.")

@login_required
def game_join(request):
    '''
        The game request process in the frontend should result in
        a json struct sent as body to an endpoint landing on 
        the game_join() view.
    '''
    if request.method != 'POST':
        return HttpResponse('A request to send a game requires a POST request with a propperly fromated body.', status=400)
    
    print('RECEIVED POST BODY : ', request.POST)
    if not request.POST:
        return HttpResponse('Trying to create a game, but either no game creation form was sent or is malformed.', status=400)


    form = GameCreationForm(request.POST)
    print('Form : \n', form)
    print('Form Errors : \n', form.errors)
    if not form.is_valid():
        return HttpResponse('Trying to create a game, but either no game creation form was sent or is missing fields.', status=400)

    print('Created form : ', form.cleaned_data['gameMode'])
    print('Created form : ', form.cleaned_data['gameType'])
    game_id = -1# default

    ### TODO: CALL GameManager to create game according to request.
    mm = app.match_maker
    print(mm)

    lobby_game = mm.join_lobby(request.user, form.cleaned_data)
    if not lobby_game:
        return HttpResponse('Joining game lobby failed.', status=400)

    payload = {
        'lobbyID': lobby_game.lobbyID,
        'gameMode': form.cleaned_data['gameMode'],
        'gameType': form.cleaned_data['gameType'],
        'withAI': form.cleaned_data['withAI'] if 'withAI' in form.cleaned_data else False
    }
    return JsonResponse(payload)
    #return render(request, 'game/game_creation_form_returned.html', {'form': form})
    #return render(request, 'game/game.html',
    #        context={
    #            'game_id': game_id
    #    }
    #)
    #return HttpResponse(f"<h1>Trying to create game with id : {game_id}</h1>")
    #return HttpResponse(f"Trying to create game with id : {game_id}")


''' Testing game instances creation '''
def _build_test_game(user: User) -> Game:
    return (Game.objects.create(
            host=user
            #group_id=f'game_{id}',
        )
    )
'''
def game_create_db_instance(request):
    id =  request.user.id
    print("id : ", id)
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return HttpResponse('Users must be logged in to be able to create games.')

    print("req user id : ", id, ", user : ", user)
    if not user: 
        return HttpResponse(f"User id {request.user.id} of requestee does not match any db entry.")

    game = _build_test_game(user=User.objects.get(id=request.user.id))
    game.save()
    return HttpResponse('Game created and pushed to database')


def game_get_state(request):
    game = Game.objects.get(id=4)
    if game:
        return HttpResponse(str(game))
    else:
        return HttpResponse(f"No game found")
    
def game_set_user_as_winner(request):
    game = Game.objects.get(id=4)
    if game:
        #request.user.winner_set.add(game)
        user = User.objects.get(id=request.user.id)
        if not user:
            return HttpResponse(f"No user found")
        #print(game.__dict__)
        #user.game_winner_set.add(game)
        game.winner = user
        game.save()
        

        #game.winner_set.add(User.objects.get(id=request.user.id))
        #game.winner = User.objects.get(id=request.user.id)
        return HttpResponse("request.user set as first game winner.")
    else:
        return HttpResponse(f"No game found")

def game_delete(request):
    game = Game.objects.get(id=4)
    if game:
        id = game.id
        game.delete()
        return HttpResponse(f"Game {id} deleted from db.")
    else:
        return HttpResponse(f"No game found")
'''


''' REDIS TESTS'''

from django_redis import get_redis_connection
import pickle
cache = get_redis_connection('default')

def redis_set_test(request, key: str, value: str):
    if not key or not value:
        return (HttpResponse('Missing key or value. Format : /game/redis/set/<key>/<value>'))

    cache.set(key, pickle.dumps(value))
    return (HttpResponse(f"Key '{key}' now set to value : " + value))


def redis_get_test(request, key: str):
    redis_get = cache.get(key)
    if not redis_get:
        return (HttpResponse(key + ' means nothing to me.'))
    print('redis_get : ', str(redis_get_big))
    big_str = pickle.loads(redis_get)
    print(big_str)
    return (HttpResponse('Value extracted from redis server : ' + big_str))


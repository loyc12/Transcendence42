from django.shortcuts import HttpResponse, render
from game.models import Game, Player, User

# Create your views here.
def game_home(request):
    print(request)
    return HttpResponse("Welcome to the game home page.")

def create_game(request, game_id: int):
    print(request)
    return render(request, 'game/game.html',
            context={
                'game_id': game_id
        }
    )
    #return HttpResponse(f"<h1>Trying to create game with id : {game_id}</h1>")
    #return HttpResponse(f"Trying to create game with id : {game_id}")


''' Testing game instances creation '''
def _build_test_game(user: User) -> Game:
    return (Game.objects.create(
            host=user
            #group_id=f'game_{id}',
        )
    )

def game_create_db_instance(request):
    id =  request.user.id
    print("id : ", id)
    user = User.objects.get(id=id)
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



''' REDIS TESTS'''
'''
from django_redis import get_redis_connection
import pickle
cache = get_redis_connection('default')

def redis_set_test(request):
    cache.set('BIG', pickle.dumps('DADDY'))
    return (HttpResponse('value set'))


def redis_get_test(request):
    redis_get_big = cache.get('BIG')
    print('redis_get_big : ', str(redis_get_big))
    big_str = pickle.loads(redis_get_big)
    print(big_str)
    if not big_str:
        return (HttpResponse('Big means nothing to me.'))
    else:
        return (HttpResponse('Value extracted from redis server : ' + big_str))
'''

from django.shortcuts import HttpResponse, render

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

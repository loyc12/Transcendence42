from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import asyncio

from game.apps import GameConfig as app
from .views import _build_error_payload
from .forms import GameEventForm

import game.PingPongRebound.Keybindings as keys

def __done_callback_for_push_event_call(*args, **kwargs):
    print('WOW !! method called as done callback for API push event !')


def __process_api_request(request, key_pressed):
    if request.method != 'POST':
        return JsonResponse(_build_error_payload('API requests are required to be POST requests.'), status=400)

    if 'apiKey' not in request.headers:
        return JsonResponse(_build_error_payload('API requests require a POST with an valid "apiKey" in headers.'), status=400)
    jsonform = {'apiKey': request.headers['apiKey']}
    ## Create and validate API request form.
    form = GameEventForm(jsonform)
    if not form.is_valid():
        return JsonResponse(_build_error_payload('Received API request, but API request form is missing fields.'), status=400)


    ## Try to send event to player game. API key will be validated in this stage.
    apiKey = form.cleaned_data['apiKey']
    game_gateway = app.get_game_gateway()

    event_loop = game_gateway.event_loop
    print('event_loop.is_running : ', event_loop.is_running())
    if not event_loop or not event_loop.is_running():
        return JsonResponse(_build_error_payload('Received API request, player is not in game.'), status=400)

    # try:
    #     event_loop = asyncio.get_event_loop()
    # except RuntimeError as exc:
    #     return JsonResponse(_build_error_payload('Received API request, player is not in game.'), status=400)


    coro = game_gateway.api_handle_event(apiKey, 'key_press', key_pressed)
    result: asyncio.Task = asyncio.ensure_future(coro, loop=event_loop)
    # if event_loop and event_loop.is_running():
    #     result = asyncio.ensure_future(coro)
    # else:
    #     result = event_loop.run_until_complete(coro)
    result.add_done_callback(__done_callback_for_push_event_call)


    ## Confirm success
    return JsonResponse({
        'status': 'success',
        'apiKey': apiKey,
        'ev': 'key_press',
        'key': key_pressed,
    })


@csrf_exempt
def api_game_press_up(request):
    return __process_api_request(request, keys.KUP)

@csrf_exempt
def api_game_press_down(request):
    return __process_api_request(request, keys.KDOWN)

@csrf_exempt
def api_game_press_left(request):
    return __process_api_request(request, keys.KLEFT)

@csrf_exempt
def api_game_press_right(request):
    return __process_api_request(request, keys.KRIGHT)


@csrf_exempt
def api_game_press_w(request):
    return __process_api_request(request, keys.KW)

@csrf_exempt
def api_game_press_s(request):
    return __process_api_request(request, keys.KS)

@csrf_exempt
def api_game_press_a(request):
    return __process_api_request(request, keys.KA)

@csrf_exempt
def api_game_press_d(request):
    return __process_api_request(request, keys.KD)


@csrf_exempt
def api_game_press_zero(request):
    return __process_api_request(request, keys.NZERO)


@csrf_exempt
def api_game_press_space(request):
    return __process_api_request(request, keys.SPACE)

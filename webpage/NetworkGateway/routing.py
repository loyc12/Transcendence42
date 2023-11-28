from django.urls import re_path
from NetworkGateway import consumers

websocket_urlpatterns = [
    re_path(r'game/ws/(?P<game_id>\w+)/$', consumers.GameConsumer.as_asgi())
]
from django.urls import re_path
from tournament import consumers

tournament_ws_urlpatterns = [
    re_path(r'tournament/ws/(?P<sock_id>\w+)/$', consumers.TournamentConsumer.as_asgi())
]
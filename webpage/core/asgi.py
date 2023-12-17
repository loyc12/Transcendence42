#ASGI config.
import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter

from NetworkGateway.consumers import GameConsumer
from users.consumers import UserConsumer
from tournament.consumers import TournamentConsumer

from django.urls import re_path


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r'game/ws/(?P<sock_id>\w+)/$', GameConsumer.as_asgi()),
                re_path(r'users/ws/(?P<sock_id>\w+)/$', UserConsumer.as_asgi()),
                re_path(r'tournament/ws/(?P<sock_id>\w+)/$', TournamentConsumer.as_asgi()),
            ])
        )
    ),
})
# DOC
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# https://asgi.readthedocs.io/en/latest/introduction.html

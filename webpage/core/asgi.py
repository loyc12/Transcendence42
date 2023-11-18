#ASGI config.

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from game.routing import websocket_urlpatterns

#It exposes the ASGI callable as a module-level variable named ``application``.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})
# DOC
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# https://asgi.readthedocs.io/en/latest/introduction.html

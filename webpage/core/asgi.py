#ASGI config.

import os
from django.core.asgi import get_asgi_application

#It exposes the ASGI callable as a module-level variable named ``application``.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
application = get_asgi_application()

# DOC
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# https://asgi.readthedocs.io/en/latest/introduction.html

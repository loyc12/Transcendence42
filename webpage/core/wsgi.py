""" WSGI config for core project. """
#WSGI config

import os
from django.core.wsgi import get_wsgi_application

# It exposes the WSGI callable as a module-level variable named ``application``.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
application = get_wsgi_application()
""" WSGI config for core project. """
# DOC
#https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/

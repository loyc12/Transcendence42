""" Django settings for webpage project. """
# Django settings (Django 4.2.6.)
# Command : django-admin startproject
# DOC
# https://docs.djangoproject.com/en/4.2/topics/settings/
# https://docs.djangoproject.com/en/4.2/ref/settings/
# https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

import os
from pathlib import Path
# from pathlib import Path
# import os
# import environ
# env = environ.Env()
# environ.Env.read_env('../.env')

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY',
                'django-insecure-%h_d1w07jpoik5d&&@$8-3*p$=f7+&s54s*laqwige$&&@gr01')

DEBUG = True # SECURITY WARNING: don't run with debug turned on in production!

SECRET_KEY = "django-insecure-%h_d1w07jpoik5d&&@$8-3*p$=f7+&s54s*laqwige$&&@gr01" 
DEBUG = True # SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = []

# NEW APPS ADDED AFTER "HOME"
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "Home",
    "frontHome",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

WSGI_APPLICATION = "core.wsgi.application"
# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# DATABASE
# if env("DG_RUN_WITH_DB"):
#     DATABASES = {
#         "default": {
#             #"ENGINE": "django.db.backends.sqlite3",
#             #"NAME": BASE_DIR / "db.sqlite3",
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": env("POSTGRES_DB"),
#             "USER": env("POSTGRES_USER"),
#             "PASSWORD": env("POSTGRES_PASSWORD"),
#             "HOST": env("DB_HOST"),
#             "PORT": env("DB_PORT")
#         }
#     }
# else:
#     DATABASES = {}

#print("Database : ")
#print(DATABASES)


#PASSWORD
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
#     },
# ]

# # HASH
# PASSWORD_HASHERS = [
#     "django.contrib.auth.hashers.Argon2PasswordHasher",
#     "django.contrib.auth.hashers.PBKDF2PasswordHasher",
#     "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
#     "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
#     "django.contrib.auth.hashers.ScryptPasswordHasher",
# ]


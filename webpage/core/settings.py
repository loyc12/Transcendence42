from pathlib import Path
import os
import subprocess
#from io import StringIO
from dotenv import load_dotenv

# AUTH0_ALEX
#import { createAuth0Client } from '@auth0/auth0-spa-js';

# ENVIRONNEMENT VAR - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
# Setting up environment variables from .env
ENV_FILE = os.environ

# Load environment variables from .env file
if not ('DJG_WITH_DB' in ENV_FILE and ENV_FILE["DJG_WITH_DB"]):
    envStream = open('../.env', 'r')
    load_dotenv(stream=envStream)
    envStream.close()
print("Environment acquired !")

SECRET_KEY = ENV_FILE["DJANGO_SECRET_KEY"]
DEBUG = True # SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# HTTPS config/protection
SECURE_HSTS_SECONDS = 3600 #31536000  # 1 year HSTS (recommended)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
#XSS protection
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True #Againts MIME sniffing
#CSP_DEFAULT_SRC = ("'self'",) # CSP policies TODO: add CSP policies
# X-Frame-Options (Against Clickjacking)
X_FRAME_OPTIONS = 'DENY' 
# Secure session management
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SECURE_SSL_REDIRECT = True

# AUTH0 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
# Get public IP from file or from shell command for OAuth2 redirect_uri
if not os.path.exists('public.ip'):
    subprocess.call(["sh", "./get_public_ip.sh", "./public.ip"])
with open('public.ip', 'r') as file:
    external_ip = file.read()
print("external IP acquired : ", external_ip)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# AUTH0_ALEX call back ?
#ENV_FILE["APP42_OAUTH_REDIRECT"] = "http://127.0.0.1"#f"{external_ip}:{ENV_FILE['DJANGO_LISTEN_PORT']}/index"#/oauth/receive_code"
# AUTH0_ALEX Logout ?
ENV_FILE["APP42_OAUTH_CONFIRM"] = f"{external_ip}:{ENV_FILE['DJANGO_LISTEN_PORT']}"#/oauth/confirm"

print("APP42_OAUTH_REDIRECT : ", ENV_FILE["APP42_OAUTH_REDIRECT"])
print("APP42_OAUTH_CONFIRM : ", ENV_FILE["APP42_OAUTH_CONFIRM"])

#  APPS - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    #"oauth2_provider",
    #"bootstrap5",
    
    "Home", 
    "oauth",
    "users"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "core.urls"


# OpenID OAuth2 config
LOGIN_URL='/admin/login/'

OAUTH2_PROVIDER = {
    "OIDC_ENABLED": True,
    "OIDC_RSA_PRIVATE_KEY": ENV_FILE["OIDC_RSA_PRIVATE_KEY"],
    "SCOPES": {
        "openid": "OpenID Connect scope",
    },
}

# AUTH0_ALEX
TEMPLATE_DIR = os.path.join(BASE_DIR, "Home", "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if "DJG_WITH_DB" in ENV_FILE and ENV_FILE["DJG_WITH_DB"]:
    DATABASES = {
        "default": {
            #"ENGINE": "django.db.backends.sqlite3",
            #"NAME": BASE_DIR / "db.sqlite3",
            "ENGINE": "django.db.backends.postgresql",
            "NAME": ENV_FILE["POSTGRES_DB"],
            "USER": ENV_FILE["POSTGRES_USER"],
            "PASSWORD": ENV_FILE["POSTGRES_PASSWORD"],
            "HOST": ENV_FILE["DB_HOST"],
            "PORT": ENV_FILE["DB_PORT"]
        }
    }
else:
    DATABASES = {}
#print("Database : ")
#print(DATABASES)


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Password hashers
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


APP42_UID = ENV_FILE["APP42_UID"]
APP42_SECRET = ENV_FILE["APP42_SECRET"]
APP42_DOMAIN = ENV_FILE["APP42_DOMAIN"]

AUTH_USER_MODEL = "users.User"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
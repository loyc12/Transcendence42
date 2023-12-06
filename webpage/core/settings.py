from pathlib import Path
import os
from dotenv import load_dotenv

#SESSION_AV
from importlib import import_module
from django.conf import settings
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore

# ENVIRONNEMENT VAR - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
ENV_FILE        = os.environ

# DJANGO_DEBUG MODE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
DJANGO_DEBUG    = not ('DJG_WITH_DB' in ENV_FILE and ENV_FILE["DJG_WITH_DB"])


# WITH NO INSTRUCTIONS IN ENV_FILE - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - |
if DJANGO_DEBUG:
    if os.path.exists('../.env'):
        envpath = '../.env'
    elif os.path.exists('./.env'):
        envpath = '.env'
    else:
        raise FileExistsError('Missing .env file.')
    with open(envpath, 'r') as envfile:
        load_dotenv(stream=envfile)


# WITH INSTRUCTIONS IN ENV_FILE  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
print("DJG_WITH_DB in env ? ", 'DJG_WITH_DB' in ENV_FILE)
if 'DJG_WITH_DB' in ENV_FILE:
    print("env['DJG_WITH_DB']) : ", ENV_FILE["DJG_WITH_DB"])
if ('DJG_WITH_DB' in ENV_FILE):
    print("DJG_WITH_DB str in env : ", ENV_FILE["DJG_WITH_DB"],\
    "len : ", len(ENV_FILE["DJG_WITH_DB"]))


# DJANGO_DEBUG = not ('DJG_WITH_DB' in ENV_FILE and ENV_FILE["DJG_WITH_DB"])
print("Environment acquired !")
print("DJANGO_DEBUG : ", DJANGO_DEBUG)


# SECURITY WARNING  - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - |
#: keep the secret key used in production secret!
DEBUG = True # SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = ENV_FILE["DJANGO_SECRET_KEY"]
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '10.12.2.10', '10.12.2.9', '10.12.2.8', '10.12.2.7', '10.12.2.6']


# APPS - - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - |
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "daphne",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django_extensions",
    "bootstrap5",
    
    "compressor",

    "Home",
    "login",
    "users",
    "channels",
    "game",
    "NetworkGateway",
]


# MIDDLEWARE - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
MIDDLEWARE = []

if not DJANGO_DEBUG:
    print("RUNNING IN ACTIVE DATABASE MODE !")
    INSTALLED_APPS += []
    MIDDLEWARE += [
        "corsheaders.middleware.CorsMiddleware",
    ]
    
MIDDLEWARE += [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

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
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = True # Should be True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SECURE_SSL_REDIRECT = True

# PATHS BUILDING - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - |
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# BAZINGA
APP42_UID       = ENV_FILE["APP42_UID"]
APP42_SECRET    = ENV_FILE["APP42_SECRET"]
APP42_DOMAIN    = ENV_FILE["APP42_DOMAIN"]

# TEMPLATE BUILDING - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|
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

AUTH_USER_MODEL = "users.User"
ROOT_URLCONF    = "core.urls"
#WSGI_APPLICATION   = "core.wsgi.application"
ASGI_APPLICATION    = "core.asgi.application"

# DATABASE  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|

if not DJANGO_DEBUG:
    DATABASES = {
        "default": {
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
print("DATABASE SETTINGS : ", DATABASES)

# AUTH PASSWORD - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -|
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

# STATIC FILES SETTINGS
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static_deploy")
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

### SESSIONS SETTINGS
SESSION_ENGINE = 'redis_sessions.session'
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_REDIS = {
    'host': ENV_FILE['REDIS_HOST'],
    'port': 6379,
    'db': 1,
    'password': ENV_FILE['REDIS_PW'],
    'prefix': 'session',
    'socket_timeout': 1,
    'retry_on_timeout': False
    }

### REDIS CACHE SETTINGS
REDIS_CACHE_URL = f"redis://:{ENV_FILE['REDIS_PW']}@{ENV_FILE['REDIS_HOST']}:6379/1"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CACHE_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

### REDIS CHANNEL LAYER SETTINGS
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_CACHE_URL)],
        },
    },
}

# COMPRESSOR SETTINGS NOT WORKING FOR NOW
COMPRESS_ENABLED = False
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
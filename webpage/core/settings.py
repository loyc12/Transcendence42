from pathlib import Path
import os

from dotenv import load_dotenv


# Setting up environment variables from .env
env = os.environ
DJG_DEBUG = not ('DJG_WITH_DB' in env and env["DJG_WITH_DB"])
if DJG_DEBUG:
    if os.path.exists('../.env'):
        envpath = '../.env'
    elif os.path.exists('./.env'):
        envpath = '.env'
    else:
        raise FileExistsError('Missing .env file.')
    with open(envpath, 'r') as envfile:
        load_dotenv(stream=envfile)

    #load_dotenv(stream=env_stream)
    #env_stream = open('../.env', 'r')
    #env_stream.close()

print("DJG_WITH_DB in env ? ", 'DJG_WITH_DB' in env)
if 'DJG_WITH_DB' in env:
    print("env['DJG_WITH_DB']) : ", env["DJG_WITH_DB"])
if ('DJG_WITH_DB' in env):
    print("DJG_WITH_DB str in env : ", env["DJG_WITH_DB"], "len : ", len(env["DJG_WITH_DB"]))
DJG_DEBUG = not ('DJG_WITH_DB' in env and env["DJG_WITH_DB"])


print("Environment acquired !")
print("DJG_DEBUG : ", DJG_DEBUG)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env["DJANGO_SECRET_KEY"]
DEBUG = True # SECURITY WARNING: don't run with debug turned on in production!
ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "daphne",
    "django.contrib.staticfiles",
    "django_extensions",
    "channels",
    #"bootstrap5",
    "Home", 
    #"oauth",
    "users",
    "game"
]

AUTH_USER_MODEL = "users.User"
MIDDLEWARE = []

if not DJG_DEBUG:
    print("RUNNING IN ACTIVE DATABASE MODE !")
    INSTALLED_APPS += [
        "oauth2_provider"
    ]

    MIDDLEWARE += [
        "corsheaders.middleware.CorsMiddleware",
    ]


MIDDLEWARE += [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "core.urls"

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


# OpenID OAuth2 config
LOGIN_URL='/admin/login/'

OAUTH2_PROVIDER = {
    "OIDC_ENABLED": True,
    "OIDC_RSA_PRIVATE_KEY": env["OIDC_RSA_PRIVATE_KEY"],
    "SCOPES": {
        "openid": "OpenID Connect scope",
    },
}

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

#WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if not DJG_DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env["POSTGRES_DB"],
            "USER": env["POSTGRES_USER"],
            "PASSWORD": env["POSTGRES_PASSWORD"],
            "HOST": env["DB_HOST"],
            "PORT": env["DB_PORT"]
        }
    }
else:
    DATABASES = {}

print("DATABASE SETTINGS : ", DATABASES)


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
STATIC_ROOT = "static_deploy/"

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


### SESSIONS SETTINGS
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


### REDIS CACHE SETTINGS
redis_cache_url = f"redis://:{env['REDIS_PW']}@{env['REDIS_HOST']}:6379/1"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": redis_cache_url,
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
            "hosts": [(redis_cache_url, )],
        },
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
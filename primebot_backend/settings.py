"""
Django settings for primebot_backend project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import errno
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret __key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY', default="")
FERNET_KEY = env.str("FERNET_SECRET_KEY", default="")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", cast=str, default=[])

# Application definition
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    # "http://127.0.0.1:8000",
    # "http://192.168.189.78:8001",
    # "http://192.168.189.78:8001",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party
    'django_extensions',
    "corsheaders",
    "django_q",
    # own
    'app_prime_league',
    'core',
    'bots',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'primebot_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 ]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'primebot_backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.str('DB_PORT'),
        'CONN_MAX_AGE': 3600,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ("de", _("German")),
    ("en", _("English")),
)

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = env.str("STATIC_ROOT", None)

GAME_SPORTS_BASE_URL = env.str("GAME_SPORTS_BASE_URL", None)

MATCH_URI = "https://www.primeleague.gg/de/leagues/matches/"
TEAM_URI = "https://www.primeleague.gg/de/leagues/teams/"
SITE_ID = env.str("SITE_ID", None)

STORAGE_DIR = os.path.join(BASE_DIR, "storage", )

TELEGRAM_BOT_KEY = env.str("TELEGRAM_BOT_API_KEY", None)
TG_DEVELOPER_GROUP = env.int("TG_DEVELOPER_GROUP", None)
TELEGRAM_START_LINK = "https://t.me/prime_league_bot?startgroup=start"

DISCORD_BOT_KEY = env.str("DISCORD_API_KEY", None)
DISCORD_APP_CLIENT_ID = env.int("DISCORD_APP_CLIENT_ID", None)
DISCORD_SERVER_LINK = "https://discord.gg/K8bYxJMDzu"

LOGIN_URL = "/admin/login/"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

LOGGING_DIR = env.str("LOGGING_DIR", "logs")
try:
    os.mkdir(LOGGING_DIR)
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise exc
    pass

DEFAULT_SCOUTING_NAME = "op.gg"
DEFAULT_SCOUTING_URL = "https://euw.op.gg/multisearch/euw?summoners={}"
DEFAULT_SCOUTING_SEP = ","

TEMP_LINK_TIMEOUT_MINUTES = 60

FILES_FROM_STORAGE = env.bool("FILES_FROM_STORAGE", False)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    } if DEBUG else {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/var/run/memcached/memcached.sock',
    }
}

LOCALE_PATHS = [
    BASE_DIR / "bots" / "locale",
    BASE_DIR / "app_prime_league" / "locale",
]

Q_CLUSTER = {
    'name': 'primebot',
    'workers': 4,  # in general the count of cpus
    'daemonize_workers': True,  #
    'recycle': 500,  # number of jobs before memory resources will be released
    'timeout': 20,  # maximum seconds for a task
    'retry': 25,  # Failed task will be queued after 25 seconds
    'max_attempts': 3,  # Maximum retry attempts for failed tasks
    'queue_limit': 50,
    'compress': False,  # Compress large payload
    'scheduler': True,  # disable schedulers reduce overhead
    'save_limit': 0,  # Limits the amount of successful tasks save to Django
    "ack_failures": True,
    'redis': {
        'host': env.str("REDIS_HOST", None),
        'port': env.str("REDIS_PORT", None),
        'password': env.str("REDIS_PASSWORD", None),
        'db': 0,
    } if DEBUG else {
        'unix_socket_path': "unix:/var/run/memcached/memcached.sock",
    }
}

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'to_file': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
            'to_console': {
                'format': '[%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': "DEBUG",
                'formatter': 'to_console',
                'class': 'logging.StreamHandler',
            },
            'django': {
                'level': "INFO",
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': os.path.join(LOGGING_DIR, 'django.log'),
                'formatter': 'to_file',
            },
            'notifications': {
                'level': 'INFO',
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': os.path.join(LOGGING_DIR, 'notifications.log'),
                'formatter': 'to_file',
            },
            'commands': {
                'level': 'INFO',
                'class': 'logging.handlers.WatchedFileHandler',
                'filename': os.path.join(LOGGING_DIR, 'commands.log'),
                'formatter': 'to_file',
            },
            'updates': {
                'level': "INFO",
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': os.path.join(LOGGING_DIR, 'updates.log'),
                'when': 'midnight',
                'formatter': 'to_file',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['django'],
                'level': "DEBUG",
                'propagate': False,
            },
            'notifications': {
                'handlers': ['notifications'],
                'level': "DEBUG",
                'propagate': False,
            },
            'commands': {
                'handlers': ['commands', ],
                'level': "INFO",
                'propagate': False,
            },
            'updates': {
                'handlers': ['updates'],
                'level': "DEBUG",
                'propagate': False,
            }
        }
    }

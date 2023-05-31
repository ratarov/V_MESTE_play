import os
from pathlib import Path

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR.parent, 'infra-vmeste/.env'), verbose=True)

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', default='False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default='*').split(', ')
DOMAIN = '127.0.0.1:8000' if DEBUG else 'v-meste.fun'


# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'meetings.apps.MeetingsConfig',
    'games.apps.GamesConfig',
    'core.apps.CoreConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'play_board.urls'

TEMPLATES_DIR = Path(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'play_board.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = Path(BASE_DIR, 'static')
# STATICFILES_DIRS = [Path(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = Path(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# OTHER SETTINGS

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'meetings:index'

INTERNAL_IPS = [
    '127.0.0.1',
]

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if not DEBUG:
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[
            DjangoIntegration(),
        ],
        traces_sample_rate=1.0,
        send_default_pii=True
    )

# EMAIL

EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


# CONSTANTS

KM_IN_DEGREE = 111
GAMES_ON_PAGE = 20
DEFAULT_SEARCH_RADIUS = 100

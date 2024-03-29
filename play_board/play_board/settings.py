import os
from pathlib import Path

import sentry_sdk
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import ignore_logger

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR.parent, 'infra-vmeste/.env'), verbose=True)

SECRET_KEY = os.getenv('SECRET_KEY', default=get_random_secret_key())
DEBUG = os.getenv('DEBUG', default='False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default='*').split(', ')
DOMAIN = '127.0.0.1:8000' if DEBUG else 'v-meste.fun'


# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'meetings.apps.MeetingsConfig',
    'games.apps.GamesConfig',
    'core.apps.CoreConfig',
    'matches.apps.MatchesConfig',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'sorl.thumbnail',
    'debug_toolbar',
    'social_django',
    'tinymce',
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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
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
        'NAME': os.getenv('DB_NAME', default='postgres'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.getenv('DB_HOST', default='db'),
        'PORT': os.getenv('DB_PORT', default=5432),
    }
}


# AUTHENTICATION
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'users.User'

SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email', 'last_name']
SOCIAL_AUTH_UUID_LENGTH = 4

SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_VK_OAUTH2_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.google.GoogleOAuth2',
]

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'meetings:index'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.user.user_details',
)

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
if not DEBUG:
    STATIC_ROOT = Path(BASE_DIR, 'static')
else:
    STATICFILES_DIRS = [Path(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = Path(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


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
MATCHES_ON_PAGE = 20
DEFAULT_SEARCH_RADIUS = 100
TESERA_GAMES_IN_REQUEST = 30


# OTHER SETTINGS

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
        send_default_pii=True,
    )
    ignore_logger("django.security.DisallowedHost")

TINYMCE_DEFAULT_CONFIG = {

    "menubar": "",
    # "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    # "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    # "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    # "language": "es_ES",  # To force a specific language instead of the Django current language.
}

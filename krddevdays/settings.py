import os

import sentry_sdk
from rest_framework.authentication import SessionAuthentication
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN', ''),
    integrations=[DjangoIntegration()]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('SECRET_KEY', 'just_random_string')

DEBUG = os.environ.get('DEBUG') == 'True'

allowed_host = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = ('*',) if allowed_host == '' else allowed_host.split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'phonenumber_field',
    'django_filters',

    'users',
    'events',
    'talks',
    'checkout',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'krddevdays.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'krddevdays.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'krddevdays'),
        'USER': os.environ.get('DB_USER', 'krddevdays'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'krddevdays'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

AUTH_USER_MODEL = 'users.User'
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


# explicitly set format because .isoformat() can return value without microseconds
REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S.%fZ',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'krddevdays.settings.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
}

STATIC_URL = '/static/'
STATIC_ROOT = './static/'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# QTickets
QTICKETS_ENDPOINT = os.environ.get('QTICKETS_ENDPOINT', '')
QTICKETS_TOKEN = os.environ.get('QTICKETS_TOKEN', '')

cors_list = os.environ.get('CORS_LIST', '')

if cors_list == '':
    CORS_ORIGIN_ALLOW_ALL = True
else:
    CORS_ORIGIN_WHITELIST = cors_list.split(',')
    CORS_ALLOW_CREDENTIALS = True

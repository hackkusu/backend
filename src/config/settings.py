"""
Django settings for Heroku Polls sample project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import environ
from google.oauth2 import service_account

root = environ.Path(__file__) - 2
env = environ.Env(DEBUG=(bool, False), )
env.read_env(env_file=root('.env'))


BASE_DIR = root()

SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=True)
HEROKU_DEPLOY = env.bool('HEROKU_DEPLOY', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


LOCAL = [
    'django_extensions',
]

PRODUCTION = [
    # 'django_s3_storage',
]

COMMON = [
    'rest_framework',
    'corsheaders'
]

APPS = [
	'polls.apps.PollsConfig',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework.authtoken',  # <-- Here
    'allauth',
    'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'graphene_django',
    'django_filters',

] + COMMON + APPS

# if DEBUG:
#     INSTALLED_APPS += LOCAL
#
# if not DEBUG:
INSTALLED_APPS += PRODUCTION

AUTHENTICATION_BACKENDS = [
    # 'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend'

    # 'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#             'https://www.googleapis.com/auth/gmail.readonly'
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'offline',
#         }
#     }
# }


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    # 'graphql_jwt.middleware.JSONWebTokenMiddleware',
]

CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_ALL_ORIGINS=True
# https://stackoverflow.com/questions/35760943/how-can-i-enable-cors-on-django-rest-framework
# https://pypi.org/project/django-cors-headers/
CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'cache-control',
    'Sec-Ch-Ua',
    'Sec-Ch-Ua-Mobile',
    'Sec-Ch-Ua-Platform',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

#
# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "http://localhost:4200",
#     "http://localhost:52234"
# ]

# CSRF_TRUSTED_ORIGINS = [
#     "http://localhost:4200",
# ]


ROOT_URLCONF = 'config.urls'

SITE_ID = 3

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

WSGI_APPLICATION = 'config.wsgi.application'

if HEROKU_DEPLOY is True:
    DATABASES = {
        'default': env.db(default='postgres://postgres:postgres@db:5432/postgres',)
    }

if HEROKU_DEPLOY is False:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'polls',
            'USER': 'polls',
            'PASSWORD': 'test1234',
            'HOST': 'localhost',
            # 'PORT': '19089'
        }
    }


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # <-- And here
    ],
}

RATELIMIT_ENABLE = True

# CORS_ORIGIN_ALLOW_ALL = True


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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# if not DEBUG:
# DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
# STATICFILES_STORAGE = 'django_s3_storage.storage.StaticS3Storage'
AWS_VIDEO_USER_REGION = 'us-west-2'  # env('AWS_REGION')
AWS_VIDEO_USER_ACCESS_KEY_ID = ''  # env('AWS_ACCESS_KEY_ID')
AWS_VIDEO_USER_SECRET_ACCESS_KEY = '' # env('AWS_SECRET_ACCESS_KEY')
# AWS_S3_BUCKET_NAME_STATIC = env('AWS_S3_BUCKET_NAME_STATIC')
# AWS_S3_BUCKET_AUTH_STATIC = False
#
STATIC_URL = '/static/'
STATIC_ROOT = (root - 1)('static')

STATICFILES_DIRS = [
    "/static",
    # BASE_DIR / "static",
    # STATIC_ROOT
    "/var/www/static/",
]

# PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
# STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = (root - 1)('media')


# storage
# GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
#     os.path.join(BASE_DIR, 'security-videos-346723-1ef9efdefc15.json')
# )
# DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
# GS_BUCKET_NAME = '00-zoot-video-queue'

AUTH_USER_MODEL='polls.User'

TOKEN_SERIALIZER='polls.TokenSerializer'

"""
Django settings for the whole project   

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import dj_database_url


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Make your own secret
SECRET_KEY = '6w%2e4g3flk67r=_pi4isrj_y%5$i22ii5a4p#&28&tf221sc_'


# SECURITY WARNING: don'_ run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.c19trace',
    'rest_framework',
    'django_filters',
    'drf_yasg',
    'django.contrib.gis',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'PAGE_SIZE': 50
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}

ROOT_URLCONF = 'apps.urls'

CUSTOM_ADMIN_PATH = os.path.realpath(
    os.path.join(os.path.dirname(__file__), '..', 'apps', 'admin')
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(CUSTOM_ADMIN_PATH, 'templates')],
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

WSGI_APPLICATION = 'wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static'


# Database using dotenv schema
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_DEFAULT_URL', 'no-database-found://'))
}

JET_DEFAULT_THEME = 'sernatur'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

STATICFILES_DIRS = (
    os.path.join(CUSTOM_ADMIN_PATH, 'static'),
)

EMAIL_BACKEND = 'django_amazon_ses.EmailBackend'

CORS_ALLOW_ALL_ORIGINS = True

USER_PASSWORD_REQUEST_EXPIRES = dict(hours=8)
USER_PASSWORD_REQUEST_MAX_PER_DAY = 8

MAIL_STATIC_BASE = os.getenv("MAIL_STATIC_BASE", None)
MAIL_FROM = os.getenv('MAIL_FROM', None)

MAIL_S3_BUCKET_NAME = os.getenv("MAIL_S3_BUCKET_NAME", None)
MAIL_S3_BUCKET_AWS_ACCESS_KEY_ID = os.getenv("MAIL_S3_BUCKET_AWS_ACCESS_KEY_ID", None)
MAIL_S3_BUCKET_AWS_SECRET_ACCESS_KEY = os.getenv("MAIL_S3_BUCKET_AWS_SECRET_ACCESS_KEY", None)

AWS_SES_ACCESS_KEY_ID = os.getenv("AWS_SES_ACCESS_KEY_ID", None)
AWS_SES_SECRET_ACCESS_KEY = os.getenv("AWS_SES_SECRET_ACCESS_KEY", None)
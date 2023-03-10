"""
Django settings for tnpapp project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
PRODUCTION = os.environ.get('PRODUCTION')
DEBUG = True if PRODUCTION is None else (PRODUCTION.lower() != "true")

ENV_ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS")
ALLOWED_HOSTS = [] if ENV_ALLOWED_HOSTS is None else ENV_ALLOWED_HOSTS.split(
    ' ')
# hardcoded allowed hosts goes here
ALLOWED_HOSTS += []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'tnpapp',
    'corsheaders', # cors headers

    'rest_framework',
    'drf_yasg',
    'user',
    'company',
    'placement'
]

CORS_ORIGIN_ALLOW_ALL = False
ENV_CORS_WHITELIST = os.environ.get("CORS_ORIGIN_WHITELIST")
CORS_ORIGIN_WHITELIST = [] if ENV_CORS_WHITELIST is None else ENV_CORS_WHITELIST.split(' ')

CSRF_TRUSTED_ORIGINS = []
if os.environ.get('CSRF_TRUSTED_ORIGINS') is not None:
    CSRF_TRUSTED_ORIGINS += os.environ['CSRF_TRUSTED_ORIGINS'].split(' ')


USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # https://whitenoise.evans.io/en/stable/django.html#enable-whitenoise
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tnpapp.urls'

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

WSGI_APPLICATION = 'tnpapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Production Static files config
STATIC_ROOT = BASE_DIR / "staticfiles"
# https://whitenoise.evans.io/en/stable/django.html#add-compression-and-caching-support
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# use the custom user model
AUTH_USER_MODEL = 'tnpapp.CustomUser'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]

# Override some variables if debug is True
# easier for development purposes
if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True 

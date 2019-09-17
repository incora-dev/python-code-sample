"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '80u_^^d70q=g9ul%sdwhou@yjhrqsm*y24_' % os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG")


ALLOWED_HOSTS = (os.environ.get("ALLOWED_HOST"), )


# Application definition

INSTALLED_APPS = [
    'djamin', #third party
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Third party
    'graphene',
    'graphene_django',
    #Custom
    'apps.base_app',
    'apps.users_app',
    'apps.projects_app',
    'apps.graphene_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'apps.jwt_auth.JWTAuthBackend', #custom
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'src.urls'

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

WSGI_APPLICATION = 'src.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASE_ROUTERS = ('apps.base_app.database_router.DefaultRouter', )

DATABASES = {
    'users_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("USERS_DB_NAME"),
        'USER': os.environ.get("USERS_DB_USER"),
        'PASSWORD': os.environ.get("USERS_DB_PASSWORD"),
        'HOST': os.environ.get("USERS_DB_HOST"),
        'PORT': os.environ.get("USERS_DB_PORT"),
    },
    'projects_db': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("PROJECTS_DB_NAME"),
        'USER': os.environ.get("PROJECTS_DB_USER"),
        'PASSWORD': os.environ.get("PROJECTS_DB_PASSWORD"),
        'HOST': os.environ.get("PROJECTS_DB_HOST"),
        'PORT': os.environ.get("PROJECTS_DB_PORT"),
    },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE")

TIME_ZONE = os.environ.get("TIME_ZONE")

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")

# GraphQL schema
GRAPHENE = {
    'SCHEMA': 'apps.graphene_app.schema.schema'
}


# JWT settings
JWT_SETTINGS = {
    'JWT_ALGORITHM': 'HS256',
    'JWT_AUDIENCE': None,
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    'JWT_ISSUER': None,
    'JWT_LEEWAY': 0,
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': False,
    'JWT_EXPIRATION_DELTA': timedelta(seconds=60 * 5),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
}

RESTORE_PASSWORD_LINK = "http://%s/restore-password?confirm_code=" % os.environ.get("ALLOWED_HOST")

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.Argon2PasswordHasher',
)

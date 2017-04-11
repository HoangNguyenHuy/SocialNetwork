import os
from . import env

# Arangodb
# SAVE_TO_ARANGODB = True
# ARANGODB_IN_TEST_MODE = False
# ARANGODB_TEST_SUBFIX = '_test'
# ARANGODB_USER = env('ARANGODB_USER')
# ARANGODB_PASS = env('ARANGODB_PASS')
# ARANGODB_HOST = env('ARANGODB_HOST')
# ARANGODB_PORT = env('ARANGODB_PORT')
# ARANGODB_NAME = env('ARANGODB_NAME')
# ARANGODB_ROOT_PASS = env('ARANGODB_ROOT_PASS')
# ARANGODB_GRAPH_NAME = env('ARANGODB_GRAPH_NAME')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!hh+!)j-5=$j1qqf6rv+4ea3mw=ewdh6mxvfo4=d$7xe-u1k45'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'SocialNetwork_API',
    'rest_framework',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sncore.urls'

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

WSGI_APPLICATION = 'sncore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases


def db_config(prefix='', test={}):
    return {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': prefix + env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASS'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'TEST': test,
        # <fix error Too many connections mysql>
        'OPTIONS': {
           "init_command": "SET GLOBAL max_connections = 100000",
        }
    }


DATABASES = {
    'default': db_config(),
    'test': db_config('test_', {'MIRROR': 'default'})
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

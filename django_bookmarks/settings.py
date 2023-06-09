"""
Django settings for django_bookmarks project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6vknpj=v2z*^%@^du5p_5)@2du0g=+sktx1n#=s)rte4&fjxlg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

SITE_REDIRECT_ORIGINAL = "http://127.0.0.1:8000"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_comments',
    'bookmarks'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.CacheMiddleware',
]

ROOT_URLCONF = 'django_bookmarks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'bookmarks/templates/bookmarks'),
            os.path.join(BASE_DIR, 'bookmarks/templates/'),
            os.path.join(BASE_DIR, 'templates/'),
        ],
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

WSGI_APPLICATION = 'django_bookmarks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'


#-------------------------------------------------------------------------
#Media settings
STATIC_ROOT=os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'
STATICFILES_DIRS=[
    
    ]
MEDIA_URL = '/media/'
MEDIA_ROOT=os.path.join(os.path.dirname(BASE_DIR),'media')
#-------------------------------------------------------------------------


from django.urls import reverse_lazy

LOGIN_REDIRECT_URL = reverse_lazy('main_page')
LOGIN_URL = reverse_lazy('login_page')
LOGOUT_URL = reverse_lazy('logout_page')


# Tag cloud
MAX_WEIGHT=5

# PAGINATION
ITEMS_PER_PAGE = 1


#Email Setting...
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'XXXX'
EMAIL_HOST_PASSWORD = 'XXXX'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "XXXX"  


# Django Translation Tools
LOCALE_PATHS = [
    os.path.join(BASE_DIR,'locale'),
]
LANGUAGE_CODE = 'de'

# CACHE_BACKEND = 'simple:///'
CACHE_BACKEND = 'db://cache_table'

# CACHE_BACKEND = 'file:///tmp/django_cache'

# CACHE_BACKEND = 'memcached://ip:port/'

CACHE_MIDDLEWARE_SECONDS = 60 * 5


ADMINS = (
    ('Your Name', 'your_email@domain.com'),
)
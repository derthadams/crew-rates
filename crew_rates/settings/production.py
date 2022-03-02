"""
Production Django settings for crew_rates project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['crew-rates-env.us-west-1.elasticbeanstalk.com', '.crewrates.org']

INSTALLED_APPS = [
    'rates.apps.RatesConfig',
    'api.apps.ApiConfig',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'invitations',
    'rest_framework',
    'captcha',
]

SITE_ID = 2

# STATIC_HOST = get_env_variable('RATES_STATIC_HOST')
# STATIC_URL = os.path.join(STATIC_HOST, 'static/')

DATABASES = {
    'default': {
        'ENGINE': get_env_variable('RATES_PROD_DATABASE_ENGINE'),
        'NAME': get_env_variable('RATES_PROD_DATABASE_NAME'),
        'USER': get_env_variable('RATES_PROD_DATABASE_USER'),
        'PASSWORD': get_env_variable('RATES_PROD_DATABASE_PASSWORD'),
        'HOST': get_env_variable('RATES_PROD_DATABASE_HOST'),
        'PORT': get_env_variable('RATES_PROD_DATABASE_PORT')
    }
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

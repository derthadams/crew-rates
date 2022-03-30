"""
Local Django settings for crew_rates project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from .base import * # noqa

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'rates.apps.RatesConfig',
    'api.apps.ApiConfig',
    'baton',
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
    'sslserver',
    'rest_framework',
    'captcha',
    'debug_toolbar',
    'baton.autodiscover',
]

SITE_ID = 1

# DATABASES = {
#     'default': {
#         'ENGINE': get_env_variable('RATES_PROD_DATABASE_ENGINE'),
#         'NAME': get_env_variable('RATES_PROD_DATABASE_NAME'),
#         'USER': get_env_variable('RATES_PROD_DATABASE_USER'),
#         'PASSWORD': get_env_variable('RATES_PROD_DATABASE_PASSWORD'),
#         'HOST': get_env_variable('RATES_PROD_DATABASE_HOST'),
#         'PORT': get_env_variable('RATES_PROD_DATABASE_PORT')
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': get_env_variable('RATES_DATABASE_ENGINE'),
        'NAME': get_env_variable('RATES_DATABASE_NAME'),
        'USER': get_env_variable('RATES_DATABASE_USER'),
        'PASSWORD': get_env_variable('RATES_DATABASE_PASSWORD'),
        'HOST': get_env_variable('RATES_DATABASE_HOST'),
        'PORT': get_env_variable('RATES_DATABASE_PORT')
    }
}


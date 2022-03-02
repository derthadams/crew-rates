"""
Production Django settings for crew_rates project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import requests
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['.crewrates.org']

EC2_PRIVATE_IP = None
try:
    security_token = requests.put(
        'http://169.254.169.254/latest/api/token',
        headers={'X-aws-ec2-metadata-token-ttl-seconds': '60'}).text

    EC2_PRIVATE_IP = requests.get(
        'http://169.254.169.254/latest/meta-data/local-ipv4',
        headers={'X-aws-ec2-metadata-token': security_token},
        timeout=0.01).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

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

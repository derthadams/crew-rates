"""
Base Django settings for crew_rates project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from django.core.exceptions import ImproperlyConfigured
from pathlib import Path


def get_env_variable(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(var_name)
        raise ImproperlyConfigured(error_msg)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable('RATES_SECRET_KEY')

LOGIN_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crew_rates.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'templates', 'allauth'),
                 os.path.join(BASE_DIR, 'templates', 'admin'),
                 os.path.join(BASE_DIR, 'templates', 'rates')
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'crew_rates.wsgi.application'

# Custom auth user model - subclasses AbstractUser
AUTH_USER_MODEL = 'rates.User'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

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

# allauth authentication backend included
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# allauth-specific configuration settings
ACCOUNT_ADAPTER = 'invitations.models.InvitationsAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_FORMS = {'login': 'rates.forms.LoginForm'}
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_ADAPTER = 'rates.adapters.DefaultSocialAccountAdapter'
SOCIALACCOUNT_FORMS = {
    'disconnect': 'rates.forms.DisconnectForm',
    'signup': 'allauth.socialaccount.forms.SignupForm',
}

# django-invitations configuration
INVITATIONS_INVITATION_ONLY = True
INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP = True
INVITATIONS_GONE_ON_ACCEPT_ERROR = False
INVITATIONS_ADAPTER = ACCOUNT_ADAPTER
INVITATIONS_EMAIL_SUBJECT_PREFIX = None
INVITATIONS_INVITATION_MODEL = 'rates.RatesInvitation'
INVITATIONS_ADMIN_ADD_FORM = 'rates.admin.RatesInvitationAdminAddForm'
INVITATIONS_ADMIN_CHANGE_FORM = 'rates.admin.RatesInvitationAdminChangeForm'
INVITATIONS_ALLOW_JSON_INVITES = True

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend', 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'us-west-2'
AWS_SES_REGION_ENDPOINT = 'email.us-west-2.amazonaws.com'
AWS_SES_CONFIGURATION_SET = get_env_variable('AWS_SES_CONFIGURATION_SET')

DEFAULT_FROM_EMAIL = "no-reply@crewrates.org"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

RECAPTCHA_PRIVATE_KEY = get_env_variable('RATES_RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_PUBLIC_KEY = get_env_variable('RATES_RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_REQUIRED_SCORE = 0.85

GRAPPELLI_ADMIN_TITLE = "Crew Rates Admin"

AUTO_APPROVE_RATE_REPORTS = True
DELETE_RAW_REPORTS_ON_APPROVAL = True

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost'
]

BATON = {
    'SITE_HEADER': 'Crew Rates',
    'SITE_TITLE': 'Crew Rates Admin',
    'COPYRIGHT': '© 2022 crewrates.org', # noqa
    'POWERED_BY': '<a href="https://www.otto.to.it">Otto srl</a>',
    'GRAVATAR_DEFAULT_IMG': 'retro',
}

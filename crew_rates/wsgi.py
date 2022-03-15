"""
WSGI config for crew_rates project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""
import newrelic.agent
newrelic.agent.initialize()
import os # noqa

from django.core.wsgi import get_wsgi_application # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crew_rates.settings')

application = get_wsgi_application()

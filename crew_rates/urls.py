"""crew_rates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from baton.autodiscover import admin
from django.contrib.flatpages import views as flatpage_views
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from django_ses.views import SESEventWebhookView
from .settings.base import get_env_variable

admin_path = get_env_variable('ADMIN_PATH')

urlpatterns = [
    # Include urls for all modules
    path('', include('rates.urls')),
    path('accounts/', include('allauth.urls')),
    path(admin_path, admin.site.urls),
    path('baton/', include('baton.urls')),
    path('api/', include('api.urls')),
    path('tos/', flatpage_views.flatpage, {'url': '/tos/'}, name='tos'),
    path('privacy/', flatpage_views.flatpage, {'url': '/privacy/'}, name='privacy'),
    path('invitations/', include('invitations.urls', namespace='invitations')),
    re_path(r'^ses/event-webhook/$', SESEventWebhookView.as_view(), name='handle-event-webhook'),
    path('__debug__', include('debug_toolbar.urls')),
]

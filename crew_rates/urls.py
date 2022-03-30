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
from django.urls import include, path

urlpatterns = [
    # Include urls for all modules
    path('', include('rates.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('baton/', include('baton.urls')),
    path('api/', include('api.urls')),
    path('tos/', flatpage_views.flatpage, {'url': '/tos/'}, name='tos'),
    path('privacy/', flatpage_views.flatpage, {'url': '/privacy/'}, name='privacy'),
    path('invitations/', include('invitations.urls', namespace='invitations')),
    path('__debug__', include('debug_toolbar.urls')),
]

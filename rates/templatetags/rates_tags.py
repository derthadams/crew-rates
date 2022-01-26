from django import template
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp, SocialAccount

register = template.Library()


@register.simple_tag
def get_app_connections(id):
    results = {
        'connected': [],
        'unconnected': []
    }
    # Get all social apps connected to the current site
    # and create a list of dicts with provider names
    social_apps = [{'name': x.name, 'id': x.provider}
                   for x in SocialApp.objects.filter(sites=Site.objects.get_current().id)]
    social_apps.sort(key=lambda x: x['id'])

    # Get the user's registered social accounts
    connected_providers = set([x.provider for x in SocialAccount.objects.filter(user_id=id)])

    for app in social_apps:
        if app['id'] in connected_providers:
            results['connected'].append(app)
        else:
            results['unconnected'].append(app)

    return results

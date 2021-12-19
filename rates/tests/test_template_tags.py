from django.apps import apps
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse

from allauth.socialaccount.models import SocialApp, SocialAccount


class TestTemplateTags(TestCase):

    def setUp(self):
        self.user_model = apps.get_model('rates', 'User')
        self.social_connections_url = reverse('socialaccount_connections')

    def test_get_app_connections(self):
        user = self.user_model.objects.create_user(email='john@google.com',
                                                   password='all3my7secrets')
        facebook = SocialApp.objects.create(provider='facebook', name='Facebook',
                                            client_id='764542658215942',
                                            secret='1fe92ff9f8417ab754d86474accf111e')
        google = SocialApp.objects.create(provider='google', name='Google',
                                          client_id='687615137298-fse5qyg7jd2m3dcu7u299rfhkc1fis3n.'
                                          'apps.googleusercontent.com',
                                          secret='Ec8ngWwrm1eeficY5zan56a1')
        twitter = SocialApp.objects.create(provider='twitter', name='Twitter',
                                           client_id='ThSeFX9HWXEhPRsBUm4iHKpDl',
                                           secret='nQrY6k5YHib2L89molFYErTy2Azh'
                                                  'UH8fNHgwEKKzelOojVphod')
        site = Site.objects.all()[0]
        facebook.sites.add(site)
        google.sites.add(site)
        twitter.sites.add(site)
        SocialAccount.objects.create(provider='facebook', user_id=user.pk)
        SocialAccount.objects.create(provider='google', user_id=user.pk)
        self.client.login(email='john@google.com', password='all3my7secrets')
        response = self.client.get(self.social_connections_url)
        self.assertContains(response, 'Remove Facebook sign in')
        self.assertContains(response, 'Remove Google sign in')
        self.assertContains(response, 'Add sign in with Twitter')

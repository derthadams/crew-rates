from django.apps import apps
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken

from rates.forms import DisconnectForm  # noqa


class TestRatesForms(TestCase):

    def setUp(self):
        self.user_model = apps.get_model('rates', 'User')
        self.social_connections_url = reverse('socialaccount_connections')

    def test_disconnect_form(self):
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

        facebook_account = SocialAccount.objects.create(provider='facebook', user_id=user.pk)
        google_account = SocialAccount.objects.create(provider='google', user_id=user.pk)
        twitter_account = SocialAccount.objects.create(provider='twitter', user_id=user.pk)

        SocialToken.objects.create(account_id=facebook_account.pk,
                                   app_id=facebook.pk, token='heresmyrandomtoken',
                                   token_secret='heresmyrandomsecret')
        SocialToken.objects.create(account_id=google_account.pk,
                                   app_id=google.pk, token='anotherrandomtoken',
                                   token_secret='heresanotherrandomsecret')
        SocialToken.objects.create(account_id=twitter_account.pk,
                                   app_id=twitter.pk, token='twitterisabovesuchthings',
                                   token_secret='itsreallynotsosecret')

        self.client.login(email='john@google.com', password='all3my7secrets')

        data = {'account': facebook_account.pk}
        facebook_accounts = SocialAccount.objects.filter(provider='facebook')
        self.assertEquals(len(facebook_accounts), 1)
        response = self.client.post(self.social_connections_url, data)
        facebook_accounts = SocialAccount.objects.filter(provider='facebook')
        self.assertEquals(len(facebook_accounts), 0)

        data = {'account': google_account.pk}
        google_accounts = SocialAccount.objects.filter(provider='google')
        self.assertEquals(len(google_accounts), 1)
        response = self.client.post(self.social_connections_url, data)
        google_accounts = SocialAccount.objects.filter(provider='google')
        self.assertEquals(len(google_accounts), 0)

        data = {'account': twitter_account.pk}
        twitter_accounts = SocialAccount.objects.filter(provider='twitter')
        self.assertEquals(len(twitter_accounts), 1)
        response = self.client.post(self.social_connections_url, data)
        twitter_accounts = SocialAccount.objects.filter(provider='twitter')
        self.assertEquals(len(twitter_accounts), 0)
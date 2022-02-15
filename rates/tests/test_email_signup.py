from django.apps import apps
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


class TestEmailSignup(TestCase):

    def setUp(self):
        self.invitation_model = apps.get_model('rates', 'RatesInvitation')
        self.user_model = apps.get_model('rates', "User")

    def test_email_signup_invitation_flow(self):
        key = "s6fg9sd8f76asd9f78a6d9g76s9fd78g9adaf79sd8f7"
        self.invitation_model.objects.create(first_name="Will", last_name="Atlas",
                                                      preferred_name="Billy",
                                                      email="will.atlas@gmail.com",
                                                      key=key, sent=timezone.now())
        invitations = self.invitation_model.objects.all()
        self.assertEqual(len(invitations), 1)
        invite_url = reverse('invitations:accept-invite',
                             kwargs={'key': key})
        response = self.client.get(invite_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertContains(response, "accepting your invitation")
        response = self.client.post(reverse('account_signup'), {'email': 'will.atlas@gmail.com',
                                                                'password1': 'grr8fl_x',
                                                                'password2': 'grr8fl_x'})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertContains(response, "Discover")
        users = self.user_model.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].email, "will.atlas@gmail.com")
        self.assertEqual(users[0].first_name, "Will")
        self.assertEqual(users[0].last_name, "Atlas")
        self.assertEqual(users[0].preferred_name, "Billy")

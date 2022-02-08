import json

from django.test import TestCase
from django.urls import reverse
from django.apps import apps


class RatesViewsTest(TestCase):

    def setUp(self):
        self.discover_url = reverse('discover')
        self.add_rate_url = reverse('add-rate')
        self.job_title = apps.get_model('rates', 'JobTitle')
        self.show = apps.get_model('rates', 'Show')
        self.network = apps.get_model('rates', 'Network')
        self.raw_rate_report = apps.get_model('rates', 'RawRateReport')
        self.user_model = apps.get_model('rates', 'User')
        self.location = apps.get_model('rates', 'Location')

    def test_index_not_logged_in(self):
        response = self.client.get(self.discover_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            '<p>To continue, sign in using your social account or email:</p>')

    def test_index_logged_in(self):
        self.user_model.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')
        response = self.client.get(self.discover_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Discover</h2>')

    def test_get_add_rate_view_logged_in(self):
        self.user_model.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')
        response = self.client.get(self.add_rate_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add a rate')

    def test_get_add_rate_view_not_logged_in(self):
        response = self.client.get(self.discover_url)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            '<p>To continue, sign in using your social account or email:</p>')

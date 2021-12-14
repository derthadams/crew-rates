from django.test import TestCase
from django.urls import reverse
from django.apps import apps


class RatesViewsTest(TestCase):

    def setUp(self):
        self.index_url = reverse('index')
        self.add_rate_url = reverse('add-rate')

    def test_index_not_logged_in(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response,
                            '<p>To continue, sign in using your social account or email:</p>')

    def test_index_logged_in(self):
        user_model = apps.get_model('rates', 'User')
        user_model.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, '<h2>Discover</h2>')

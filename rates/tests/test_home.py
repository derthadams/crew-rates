from django.test import TestCase
from django.urls import reverse


class TestHome(TestCase):
    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Negotiate better rates using crowdsourced')

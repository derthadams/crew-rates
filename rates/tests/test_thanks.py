from django.test import TestCase
from django.urls import reverse


class TestThanks(TestCase):
    def test_thanks(self):
        response = self.client.get(reverse('thanks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Thanks!')

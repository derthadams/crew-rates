from django.test import TestCase
from django.urls import reverse
from django.apps import apps


class TestSeasonListAPIView(TestCase):

    def setUp(self):
        self.user_model = apps.get_model('rates', 'User')
        self.season_list_url = reverse('season-list')

    def create_user_and_log_in(self):
        self.user_model.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')


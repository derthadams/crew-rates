from django.test import TestCase
from django.urls import reverse
from django.apps import apps

'''
- Create 5 seasons:
    - 3 IA, 1 non-union, 1 NABET
    - 4 reality, 1 game show
    - Date spread:
        - < 6 mo (2)
        - > 6 mo/ < 12 mo (1)
        - > 12 mo/ < 24 mo (1)
        - > 24 mo (1)
'''


class TestSeasonListAPIView(TestCase):

    def setUp(self):
        self.user_model = apps.get_model('rates', 'User')
        self.season_list_url = reverse('season-list')

    def create_user_and_log_in(self):
        self.user_model.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')


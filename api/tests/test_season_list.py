import json

from django.test import TestCase
from django.urls import reverse
from django.apps import apps

from rates.models import Company, JobTitle, Network, RateReport, RawRateReport, Show, User # noqa

from .sample_data import *

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
    def create_user_and_log_in(self):
        User.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')

    def populate_reports(self):
        self.create_user_and_log_in()
        self.client.post(self.add_rate_url, content_type='application/json',
                                    data=runway_report)
        self.client.post(self.add_rate_url, content_type='application/json',
                         data=wipeout_report)
        self.client.post(self.add_rate_url, content_type='application/json',
                         data=love_is_blind_report)
        self.client.post(self.add_rate_url, content_type='application/json',
                         data=real_housewives_report)
        self.client.post(self.add_rate_url, content_type='application/json',
                         data=price_is_right_report)

    @classmethod
    def setUpTestData(cls):
        cls.season_list_url = reverse('season-list')
        cls.add_rate_url = reverse('add-rate-api')

        Show.objects.create(**runway_show) # noqa
        Show.objects.create(**wipeout_show)
        Show.objects.create(**love_is_blind_show)
        Show.objects.create(**real_housewives_show)
        Show.objects.create(**price_is_right_show)

        Company.objects.create(**magical_elves) # noqa
        Company.objects.create(**endemol)
        Company.objects.create(**kinetic) # noqa
        Company.objects.create(**evolution)
        Company.objects.create(**fremantle)

        Network.objects.create(**bravo)
        Network.objects.create(**tbs)
        Network.objects.create(**netflix)
        Network.objects.create(**cbs)

        JobTitle.objects.create(**operator)

    def test_no_params(self):
        self.populate_reports()
        response = self.client.get(self.season_list_url, {'date_range': 0, 'union_select': 'AA',
                                                          'genre_select': 'AA'})
        shows = Show.objects.all()
        print(f"number of shows: {len(shows)}")
        rate_reports = RateReport.objects.all()
        print(f"number of rate reports: {len(rate_reports)}")
        raw_rate_reports = RawRateReport.objects.all()
        print(f"number of raw rate reports: {len(raw_rate_reports)}")
        response_data = json.loads(response.content)
        print(response_data)

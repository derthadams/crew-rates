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


class TestDiscoverAPIViews(TestCase):
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
        cls.summary_url = reverse('summary')
        cls.filter_search_url = reverse('filter-search')

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
        JobTitle.objects.create(**assistant)

    def test_season_list_no_params(self):
        self.populate_reports()
        response = self.client.get(self.season_list_url, {'date_range': 0, 'union_select': 'AA',
                                                          'genre_select': 'AA'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 5)

    def test_season_list_six_months_only(self):
        self.populate_reports()
        response = self.client.get(self.season_list_url, {'date_range': 6, 'union_select': 'AA',
                                                          'genre_select': 'AA'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 2)

    def test_season_list_six_months_ia(self):
        self.populate_reports()
        response = self.client.get(self.season_list_url, {'date_range': 6, 'union_select': 'IA',
                                                          'genre_select': 'AA'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 2)

    def test_season_list_twelve_months_ia(self):
        self.populate_reports()
        response = self.client.get(self.season_list_url, {'date_range': 12, 'union_select': 'IA',
                                                          'genre_select': 'AA'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 3)

    def test_season_list_ia_only(self):
        self.populate_reports()
        response = self.client.get(self.season_list_url, {'date_range': 0, 'union_select': 'IA',
                                                          'genre_select': 'AA'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 3)

    def test_season_list_reality_only(self):
        self.populate_reports()
        response = self.client.get(self.season_list_url, {'date_range': 0, 'union_select': 'AA',
                                                          'genre_select': 'RE'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 4)

    def test_season_list_no_reality(self):
        self.populate_reports()
        response = self.client.get(self.season_list_url, {'date_range': 0, 'union_select': 'NO',
                                                          'genre_select': 'RE'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 1)

    def test_season_list_twelve_months_reality(self):
        self.populate_reports()
        response = self.client.get(self.season_list_url, {'date_range': 12, 'union_select': 'AA',
                                                          'genre_select': 'RE'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 3)

    def test_season_list_two_years_no_reality(self):
        self.populate_reports()
        response = self.client.get(self.season_list_url, {'date_range': 24, 'union_select': 'NO',
                                                          'genre_select': 'RE'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 1)

    def test_season_list_operator_only(self):
        self.populate_reports() # noqa
        response = self.client.get(self.season_list_url,
                                   {'date_range': 0, 'union_select': 'AA', 'genre_select': 'AA',
                                    'filter_type': 'Job Title',
                                    'filter_uuid': '5c09a673-d0c7-481f-8500-36c581bd7b4e'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 4)

    def test_season_list_runway_only(self):
        self.populate_reports() # noqa
        response = self.client.get(self.season_list_url,
                                   {'date_range': 0, 'union_select': 'AA', 'genre_select': 'AA',
                                    'filter_type': 'Show',
                                    'filter_uuid': '48a6f024-2aa1-4f29-8db0-de0454385a2c'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 1)

    def test_season_list_bravo_only(self):
        self.populate_reports() # noqa
        response = self.client.get(self.season_list_url,
                                   {'date_range': 0, 'union_select': 'AA', 'genre_select': 'AA',
                                    'filter_type': 'Network',
                                    'filter_uuid': 'a7f641e0-bbfc-4469-9acd-404f2c8b923f'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 2)

    def test_season_list_endemol_only(self):
        self.populate_reports() # noqa
        response = self.client.get(self.season_list_url,
                                   {'date_range': 0, 'union_select': 'AA', 'genre_select': 'AA',
                                    'filter_type': 'Company',
                                    'filter_uuid': 'caf6966d-a961-4a57-8872-39a4f51ce798'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['results']), 1)

    def test_summary_operator_no_params(self):
        self.populate_reports() # noqa
        response = self.client.get(self.summary_url,
                                   {'date_range': 0, 'union_select': 'AA', 'genre_select': 'AA',
                                    'filter_type': 'Job Title',
                                    'filter_uuid': '5c09a673-d0c7-481f-8500-36c581bd7b4e'})
        response_data = json.loads(response.content)
        self.assertEqual(response_data['rate_count'], 4)
        self.assertEqual(response_data['histogram']['med'], 63.6363)

    def test_summary_operator_reality(self):
        self.populate_reports() # noqa
        response = self.client.get(self.summary_url,
                                   {'date_range': 0, 'union_select': 'AA', 'genre_select': 'RE',
                                    'filter_type': 'Job Title',
                                    'filter_uuid': '5c09a673-d0c7-481f-8500-36c581bd7b4e'})
        response_data = json.loads(response.content)
        self.assertEqual(response_data['rate_count'], 3)
        self.assertEqual(response_data['histogram']['med'], 63.6363)

    def test_summary_operator_ia(self):
        self.populate_reports() # noqa
        response = self.client.get(self.summary_url,
                                   {'date_range': 0, 'union_select': 'IA', 'genre_select': 'AA',
                                    'filter_type': 'Job Title',
                                    'filter_uuid': '5c09a673-d0c7-481f-8500-36c581bd7b4e'})
        response_data = json.loads(response.content)
        self.assertEqual(response_data['rate_count'], 2)
        self.assertEqual(response_data['histogram']['med'], 63.6363)

    def test_filter_search_no_query(self):
        self.populate_reports()
        response = self.client.get(self.filter_search_url,
                                   {'q': ''})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 0)

    def test_filter_search_c(self):
        self.populate_reports()
        response = self.client.get(self.filter_search_url,
                                   {'q': 'c'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 8)

    def test_filter_search_ca(self):
        self.populate_reports()
        response = self.client.get(self.filter_search_url,
                                   {'q': 'ca'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 4)

    def test_filter_search_cam(self):
        self.populate_reports()
        response = self.client.get(self.filter_search_url,
                                   {'q': 'cam'})
        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 2)

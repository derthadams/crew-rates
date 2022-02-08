import json
import uuid

from django.test import TestCase
from django.urls import reverse
from django.apps import apps


class APIViewsTest(TestCase):

    def create_user_and_log_in(self):
        self.user_model.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')

    def setUp(self):
        self.job_title = apps.get_model('rates', 'JobTitle')
        self.show = apps.get_model('rates', 'Show')
        self.company = apps.get_model('rates', 'Company')
        self.network = apps.get_model('rates', 'Network')
        self.user_model = apps.get_model('rates', 'User')
        self.raw_rate_report = apps.get_model('rates', 'RawRateReport')
        self.job_title_url = reverse('job-titles')
        self.show_url = reverse('shows')
        self.company_url = reverse('companies')
        self.network_url = reverse('networks')
        self.autocomplete_url = reverse('autocomplete')
        self.details_url = reverse('details')
        self.add_rate_url = reverse('add-rate-api')
        self.sessiontoken = uuid.uuid4()

    def test_no_job_titles(self):
        self.create_user_and_log_in()
        response = self.client.get(self.job_title_url + '?q=camera')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_one_job_title(self):
        self.create_user_and_log_in()
        self.job_title.objects.get_or_create(title='camera operator')
        url = reverse('job-titles')
        response = self.client.get(self.job_title_url + '?q=camera')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_two_job_titles(self):
        self.create_user_and_log_in()
        self.job_title.objects.get_or_create(title='camera operator')
        self.job_title.objects.get_or_create(title='camera assistant')
        url = reverse('job-titles')
        response = self.client.get(self.job_title_url + '?q=camera')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_job_titles_no_match(self):
        self.create_user_and_log_in()
        self.job_title.objects.get_or_create(title='director of photography')
        self.job_title.objects.get_or_create(title='steadicam operator')
        url = reverse('job-titles')
        response = self.client.get(self.job_title_url + '?q=camera')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_job_titles_not_logged_in(self):
        self.job_title.objects.get_or_create(title='camera operator')
        url = reverse('job-titles')
        response = self.client.get(self.job_title_url + '?q=camera')
        self.assertEqual(response.status_code, 403)
        all_reports = self.raw_rate_report.objects.all()
        self.assertEqual(len(all_reports), 0)

    def test_no_shows(self):
        self.create_user_and_log_in()
        response = self.client.get(self.show_url + '?q=housewives')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_one_show(self):
        self.create_user_and_log_in()
        self.show.objects.get_or_create(title='Real Housewives of Beverly Hills')
        response = self.client.get(self.show_url + '?q=housewives')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_two_shows(self):
        self.create_user_and_log_in()
        self.show.objects.get_or_create(title='Real Housewives of New Jersey')
        self.show.objects.get_or_create(title='Real Housewives of Atlanta')
        response = self.client.get(self.show_url + '?q=housewives')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_shows_no_match(self):
        self.create_user_and_log_in()
        self.show.objects.get_or_create(title='Survivor')
        self.show.objects.get_or_create(title='24 Hours to Hell and Back')
        response = self.client.get(self.show_url + '?q=runway')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_one_show_not_logged_in(self):
        self.show.objects.get_or_create(title='Real Housewives of Beverly Hills')
        response = self.client.get(self.show_url + '?q=housewives')
        self.assertEqual(response.status_code, 403)

    def test_no_companies(self):
        self.create_user_and_log_in()
        response = self.client.get(self.company_url + '?q=endemol')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_one_company(self):
        self.create_user_and_log_in()
        self.company.objects.get_or_create(name='EndemolShine NorthAmerica')
        response = self.client.get(self.company_url + '?q=endemol')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_two_companies(self):
        self.create_user_and_log_in()
        self.company.objects.get_or_create(name='Magical Elves, LLC')
        self.company.objects.get_or_create(name='Open 4 Business, LLC')
        response = self.client.get(self.company_url + '?q=llc')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_companies_no_match(self):
        self.create_user_and_log_in()
        self.company.objects.get_or_create(name='A. Smith & Co.')
        self.company.objects.get_or_create(name='Fremantle Media')
        response = self.client.get(self.company_url + '?q=burnett')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_one_company_not_logged_in(self):
        self.company.objects.get_or_create(name='EndemolShine NorthAmerica')
        response = self.client.get(self.company_url + '?q=endemol')
        self.assertEqual(response.status_code, 403)

    def test_no_networks(self):
        self.create_user_and_log_in()
        response = self.client.get(self.network_url + '?q=nbc')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_one_network(self):
        self.create_user_and_log_in()
        self.network.objects.get_or_create(name='Netflix')
        response = self.client.get(self.network_url + '?q=net')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_two_networks(self):
        self.create_user_and_log_in()
        self.network.objects.get_or_create(name='NBC')
        self.network.objects.get_or_create(name='ABC')
        response = self.client.get(self.network_url + '?q=bc')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)

    def test_networks_no_match(self):
        self.create_user_and_log_in()
        self.network.objects.get_or_create(name='HBO Max')
        self.network.objects.get_or_create(name='Disney+')
        response = self.client.get(self.network_url + '?q=apple')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 0)

    def test_one_network_not_logged_in(self):
        self.network.objects.get_or_create(name='Netflix')
        response = self.client.get(self.network_url + '?q=net')
        self.assertEqual(response.status_code, 403)

    def test_autocomplete(self):
        self.create_user_and_log_in()
        params = {
            'q': 'burbank',
            'sessiontoken': str(self.sessiontoken)
        }
        response = self.client.get(self.autocomplete_url, params)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Burbank')

    def test_details(self):
        self.create_user_and_log_in()
        params = {
            'q': 'ChIJlcUYKBWVwoAR1IofkK-RdzA',
            'sessiontoken': str(self.sessiontoken)
        }
        response = self.client.get(self.details_url, params)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'California')

    def test_add_rate_post_with_valid_json(self):
        self.user_model.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')
        ajax_form_dict = {
            "show": "dba9eb69-ca1f-4040-8215-95635d3643fd",
            "show_title": "Project Greenlight",
            "season_number": 6,
            "companies": [
                {
                    "uuid": "caf6966d-a961-4a57-8872-39a4f51ce798",
                    "name": "EndemolShine NorthAmerica"
                }
            ],
            "network": "8eb7ab01-e38a-469c-b792-3d5e7469dc86",
            "network_name": "HBO Max",
            "genre": "RE",
            "union": "IA",
            "locations": [
                {
                    "display_name": "Los Angeles, CA, USA",
                    "latitude": "34.0522342",
                    "longitude": "-118.2436849",
                    "scopes": [
                        {
                            "long_name": "Los Angeles",
                            "short_name": "Los Angeles",
                            "type": "locality",
                            "display_name": "Los Angeles, CA, US"
                        },
                        {
                            "long_name": "Los Angeles County",
                            "short_name": "Los Angeles County",
                            "type": "administrative_area_level_2",
                            "display_name": "Los Angeles County, CA, US"
                        },
                        {
                            "long_name": "California",
                            "short_name": "CA",
                            "type": "administrative_area_level_1",
                            "display_name": "California, US"
                        },
                        {
                            "long_name": "United States",
                            "short_name": "US",
                            "type": "country",
                            "display_name": "United States"
                        }
                    ]
                }
            ],
            "start_date": "2022-01-01",
            "end_date": "2022-01-31",
            "job_title": "5c09a673-d0c7-481f-8500-36c581bd7b4e",
            "job_title_name": "Camera Operator",
            "offered_hourly": 50,
            "offered_guarantee": 12,
            "negotiated": True,
            "increased": True,
            "final_hourly": 72.7273,
            "final_guarantee": 10
        }
        response = self.client.post(self.add_rate_url, content_type="application/json",
                                    data=ajax_form_dict)
        self.assertEqual(response.status_code, 201)
        all_reports = self.raw_rate_report.objects.all()
        self.assertEqual(len(all_reports), 1)
        # print(all_reports[0])

    def test_add_rate_post_with_invalid_json_missing_fields(self):
        self.user_model.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')
        ajax_form_dict = {
            "show": "dba9eb69-ca1f-4040-8215-95635d3643fd",
            "show_title": "Project Greenlight",
            "season_number": 6,
            "companies": [
                {
                    "uuid": "caf6966d-a961-4a57-8872-39a4f51ce798",
                    "name": "EndemolShine NorthAmerica"
                }
            ],
            "network": "8eb7ab01-e38a-469c-b792-3d5e7469dc86",
            "network_name": "HBO Max",
            "genre": "RE",
            "union": "IA",
            "locations": [
                {
                    "display_name": "Los Angeles, CA, USA",
                    "latitude": "34.0522342",
                    "longitude": "-118.2436849",
                    "scopes": [
                        {
                            "long_name": "Los Angeles",
                            "short_name": "Los Angeles",
                            "type": "locality",
                            "display_name": "Los Angeles, CA, US"
                        },
                        {
                            "long_name": "Los Angeles County",
                            "short_name": "Los Angeles County",
                            "type": "administrative_area_level_2",
                            "display_name": "Los Angeles County, CA, US"
                        },
                        {
                            "long_name": "California",
                            "short_name": "CA",
                            "type": "administrative_area_level_1",
                            "display_name": "California, US"
                        },
                        {
                            "long_name": "United States",
                            "short_name": "US",
                            "type": "country",
                            "display_name": "United States"
                        }
                    ]
                }
            ],
            "start_date": "2022-01-01",
            "end_date": "2022-01-31",
            "offered_hourly": 50,
            "offered_guarantee": 12,
            "negotiated": False,
            "increased": "",
            "final_hourly": "",
            "final_guarantee": ""
        }
        response = self.client.post(self.add_rate_url, content_type="application/json",
                                    data=ajax_form_dict)
        self.assertEqual(response.status_code, 400)
        # print(f"data: {response.data}")
        # print(f"content: {response.content}")
        all_reports = self.raw_rate_report.objects.all()
        self.assertEqual(len(all_reports), 0)

    def test_add_rate_post_not_logged_in(self):
        ajax_form_dict = {
            "show": "dba9eb69-ca1f-4040-8215-95635d3643fd",
            "show_title": "Project Greenlight",
            "season_number": 6,
            "companies": [
                {
                    "uuid": "caf6966d-a961-4a57-8872-39a4f51ce798",
                    "name": "EndemolShine NorthAmerica"
                }
            ],
            "network": "8eb7ab01-e38a-469c-b792-3d5e7469dc86",
            "network_name": "HBO Max",
            "genre": "RE",
            "union": "IA",
            "locations": [
                {
                    "display_name": "Los Angeles, CA, USA",
                    "latitude": "34.0522342",
                    "longitude": "-118.2436849",
                    "scopes": [
                        {
                            "long_name": "Los Angeles",
                            "short_name": "Los Angeles",
                            "type": "locality",
                            "display_name": "Los Angeles, CA, US"
                        },
                        {
                            "long_name": "Los Angeles County",
                            "short_name": "Los Angeles County",
                            "type": "administrative_area_level_2",
                            "display_name": "Los Angeles County, CA, US"
                        },
                        {
                            "long_name": "California",
                            "short_name": "CA",
                            "type": "administrative_area_level_1",
                            "display_name": "California, US"
                        },
                        {
                            "long_name": "United States",
                            "short_name": "US",
                            "type": "country",
                            "display_name": "United States"
                        }
                    ]
                }
            ],
            "start_date": "2022-01-01",
            "end_date": "2022-01-31",
            "job_title": "5c09a673-d0c7-481f-8500-36c581bd7b4e",
            "job_title_name": "Camera Operator",
            "offered_hourly": 50,
            "offered_guarantee": 12,
            "negotiated": True,
            "increased": True,
            "final_hourly": 72.7273,
            "final_guarantee": 10
        }
        response = self.client.post(self.add_rate_url, content_type="application/json",
                                    data=ajax_form_dict)
        self.assertEqual(response.status_code, 403)
        all_reports = self.raw_rate_report.objects.all()
        self.assertEqual(len(all_reports), 0)


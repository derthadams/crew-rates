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
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 0)

    def test_one_job_title(self):
        self.create_user_and_log_in()
        self.job_title.objects.get_or_create(title='camera operator')
        url = reverse('job-titles')
        response = self.client.get(self.job_title_url + '?q=camera')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 1)

    def test_two_job_titles(self):
        self.create_user_and_log_in()
        self.job_title.objects.get_or_create(title='camera operator')
        self.job_title.objects.get_or_create(title='camera assistant')
        url = reverse('job-titles')
        response = self.client.get(self.job_title_url + '?q=camera')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 2)

    def test_job_titles_no_match(self):
        self.create_user_and_log_in()
        self.job_title.objects.get_or_create(title='director of photography')
        self.job_title.objects.get_or_create(title='steadicam operator')
        url = reverse('job-titles')
        response = self.client.get(self.job_title_url + '?q=camera')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 0)

    def test_no_shows(self):
        self.create_user_and_log_in()
        response = self.client.get(self.show_url + '?q=housewives')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 0)

    def test_one_show(self):
        self.create_user_and_log_in()
        self.show.objects.get_or_create(title='Real Housewives of Beverly Hills')
        response = self.client.get(self.show_url + '?q=housewives')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 1)

    def test_two_shows(self):
        self.create_user_and_log_in()
        self.show.objects.get_or_create(title='Real Housewives of New Jersey')
        self.show.objects.get_or_create(title='Real Housewives of Atlanta')
        response = self.client.get(self.show_url + '?q=housewives')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 2)

    def test_shows_no_match(self):
        self.create_user_and_log_in()
        self.show.objects.get_or_create(title='Survivor')
        self.show.objects.get_or_create(title='24 Hours to Hell and Back')
        response = self.client.get(self.show_url + '?q=runway')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 0)

    def test_no_companies(self):
        response = self.client.get(self.company_url + '?q=endemol')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 0)

    def test_one_company(self):
        self.company.objects.get_or_create(name='EndemolShine NorthAmerica')
        response = self.client.get(self.company_url + '?q=endemol')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 1)

    def test_two_companies(self):
        self.company.objects.get_or_create(name='Magical Elves, LLC')
        self.company.objects.get_or_create(name='Open 4 Business, LLC')
        response = self.client.get(self.company_url + '?q=llc')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 2)

    def test_companies_no_match(self):
        self.company.objects.get_or_create(name='A. Smith & Co.')
        self.company.objects.get_or_create(name='Fremantle Media')
        response = self.client.get(self.company_url + '?q=burnett')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 0)

    def test_no_networks(self):
        response = self.client.get(self.network_url + '?q=nbc')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 0)

    def test_one_network(self):
        self.network.objects.get_or_create(name='Netflix')
        response = self.client.get(self.network_url + '?q=net')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 1)

    def test_two_networks(self):
        self.network.objects.get_or_create(name='NBC')
        self.network.objects.get_or_create(name='ABC')
        response = self.client.get(self.network_url + '?q=bc')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 2)

    def test_networks_no_match(self):
        self.network.objects.get_or_create(name='HBO Max')
        self.network.objects.get_or_create(name='Disney+')
        response = self.client.get(self.network_url + '?q=apple')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 0)

    def test_autocomplete(self):
        params = {
            'q': 'burbank',
            'sessiontoken': str(self.sessiontoken)
        }
        response = self.client.get(self.autocomplete_url, params)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Burbank')

    def test_details(self):
        params = {
            'q': 'ChIJlcUYKBWVwoAR1IofkK-RdzA',
            'sessiontoken': str(self.sessiontoken)
        }
        response = self.client.get(self.details_url, params)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'California')

    def test_add_rate_post_with_valid_json(self):
        self.user_model.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')
        ajax_form_dict = {
            "job_title": '5c09a673-d0c7-481f-8500-36c581bd7b4e',
            "job_title_name": "Camera Operator",
            "hourly": 54.5454,
            "guarantee": 10,
            "show": '48a6f024-2aa1-4f29-8db0-de0454385a2c',
            "show_title": "Project Runway",
            "season_number": 4,
            "companies": [{"uuid": "0fa1f64b-58d6-4963-914c-b0711c70e051",
                           "name": "Magical Elves"}],
            "network": 'a7f641e0-bbfc-4469-9acd-404f2c8b923f',
            "network_name": "Bravo",
            "locations":
                [{
                    "display_name": "Los Angeles, CA, US",
                    "scopes": [
                        {
                            "display_name": "Los Angeles, CA, US",
                            "long_name": "Los Angeles",
                            "short_name": "Los Angeles",
                            "type": "locality"
                        },
                        {
                            "display_name": "Los Angeles County, CA, US",
                            "long_name": "Los Angeles County",
                            "short_name": "Los Angeles County",
                            "type": "administrative_area_level_2"
                        },
                        {
                            "display_name": "California, US",
                            "long_name": "California",
                            "short_name": "CA",
                            "type": "administrative_area_level_1"
                        },
                        {
                            "display_name": "United States",
                            "long_name": "United States",
                            "short_name": "US",
                            "type": "country"
                        },

                    ]
                }],
            "start_date": "2021-01-01",
            "end_date": "2021-02-01",
            "union": "IA",
            "genre": "RE",
        }
        response = self.client.post(self.add_rate_url, content_type="application/json",
                                    data=ajax_form_dict)
        self.assertEquals(response.status_code, 201)
        all_reports = self.raw_rate_report.objects.all()
        self.assertEquals(len(all_reports), 1)
        # print(all_reports[0])

    def test_add_rate_post_with_invalid_json_missing_fields(self):
        self.user_model.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')
        ajax_form_dict = {
            "hourly": 54.5454,
            "guarantee": 10,
            "show": '48a6f024-2aa1-4f29-8db0-de0454385a2c',
            "show_title": "Project Runway",
            "season_number": 4,
            "companies": [{"uuid": "0fa1f64b-58d6-4963-914c-b0711c70e051",
                           "name": "Magical Elves"}],
            "network": 'a7f641e0-bbfc-4469-9acd-404f2c8b923f',
            "network_name": "Bravo",
            "locations":
                [{
                    "display_name": "Los Angeles, CA, US",
                    "scopes": [
                        {
                            "display_name": "Los Angeles, CA, US",
                            "long_name": "Los Angeles",
                            "short_name": "Los Angeles",
                            "type": "locality"
                        },
                        {
                            "display_name": "Los Angeles County, CA, US",
                            "long_name": "Los Angeles County",
                            "short_name": "Los Angeles County",
                            "type": "administrative_area_level_2"
                        },
                        {
                            "display_name": "California, US",
                            "long_name": "California",
                            "short_name": "CA",
                            "type": "administrative_area_level_1"
                        },
                        {
                            "display_name": "United States",
                            "long_name": "United States",
                            "short_name": "US",
                            "type": "country"
                        },

                    ]
                }],
            "start_date": "2021-01-01",
            "end_date": "2021-02-01",
            "union": "IA",
            "genre": "RE",
        }
        response = self.client.post(self.add_rate_url, content_type="application/json",
                                    data=ajax_form_dict)
        self.assertEquals(response.status_code, 400)
        # print(f"data: {response.data}")
        # print(f"content: {response.content}")
        all_reports = self.raw_rate_report.objects.all()
        self.assertEquals(len(all_reports), 0)

    def test_add_rate_post_not_logged_in(self):
        ajax_form_dict = {
            "job_title": '5c09a673-d0c7-481f-8500-36c581bd7b4e',
            "job_title_name": "Camera Operator",
            "hourly": 54.5454,
            "guarantee": 10,
            "show": '48a6f024-2aa1-4f29-8db0-de0454385a2c',
            "show_title": "Project Runway",
            "season_number": 4,
            "companies": [{"uuid": "0fa1f64b-58d6-4963-914c-b0711c70e051",
                           "name": "Magical Elves"}],
            "network": 'a7f641e0-bbfc-4469-9acd-404f2c8b923f',
            "network_name": "Bravo",
            "locations":
                [{
                    "display_name": "Los Angeles, CA, US",
                    "scopes": [
                        {
                            "display_name": "Los Angeles, CA, US",
                            "long_name": "Los Angeles",
                            "short_name": "Los Angeles",
                            "type": "locality"
                        },
                        {
                            "display_name": "Los Angeles County, CA, US",
                            "long_name": "Los Angeles County",
                            "short_name": "Los Angeles County",
                            "type": "administrative_area_level_2"
                        },
                        {
                            "display_name": "California, US",
                            "long_name": "California",
                            "short_name": "CA",
                            "type": "administrative_area_level_1"
                        },
                        {
                            "display_name": "United States",
                            "long_name": "United States",
                            "short_name": "US",
                            "type": "country"
                        },

                    ]
                }],
            "start_date": "2021-01-01",
            "end_date": "2021-02-01",
            "union": "IA",
            "genre": "RE",
        }
        response = self.client.post(self.add_rate_url, content_type="application/json",
                                    data=ajax_form_dict)
        self.assertEquals(response.status_code, 403)
        all_reports = self.raw_rate_report.objects.all()
        self.assertEquals(len(all_reports), 0)


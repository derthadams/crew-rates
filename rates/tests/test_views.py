import json

from django.test import TestCase
from django.urls import reverse
from django.apps import apps


class RatesViewsTest(TestCase):

    def setUp(self):
        self.index_url = reverse('index')
        self.add_rate_url = reverse('add-rate')
        self.job_title = apps.get_model('rates', 'JobTitle')
        self.show = apps.get_model('rates', 'Show')
        self.network = apps.get_model('rates', 'Network')
        self.raw_rate_report = apps.get_model('rates', 'RawRateReport')
        self.user_model = apps.get_model('rates', 'User')
        self.location = apps.get_model('rates', 'Location')

    def test_index_not_logged_in(self):
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response,
                            '<p>To continue, sign in using your social account or email:</p>')

    def test_index_logged_in(self):
        self.user_model.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')
        response = self.client.get(self.index_url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, '<h2>Discover</h2>')

    def test_add_rate_post_with_valid_json(self):
        self.user_model.objects.create_user(email='john@gmail.com', password='super-secret')
        self.client.login(email='john@gmail.com', password='super-secret')
        self.job_title.objects.get_or_create(title='Camera Operator',
                                             uuid='5c09a673-d0c7-481f-8500-36c581bd7b4e')
        self.show.objects.get_or_create(title='Project Runway',
                                        uuid='48a6f024-2aa1-4f29-8db0-de0454385a2c')
        self.network.objects.get_or_create(name='Bravo',
                                           uuid='a7f641e0-bbfc-4469-9acd-404f2c8b923f')
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
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/thanks/')
        all_reports = self.raw_rate_report.objects.all()
        self.assertEquals(len(all_reports), 1)


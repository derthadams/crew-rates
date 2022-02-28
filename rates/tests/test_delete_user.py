from django.test import TestCase
from django.urls import reverse
from django.apps import apps

from .sample_data import valid_json


class DeleteUserTest(TestCase):

    def setUp(self):
        self.add_rate_url = reverse('add-rate-api')
        self.settings_url = reverse('settings')
        self.user_model = apps.get_model('rates', 'User')
        self.rate_report = apps.get_model('rates', 'RateReport')
        self.raw_rate_report = apps.get_model('rates', 'RawRateReport')
        self.job_title = apps.get_model('rates', 'JobTitle') # noqa
        self.show = apps.get_model('rates', 'Show')
        self.company = apps.get_model('rates', 'Company')
        self.network = apps.get_model('rates', 'Network')
        self.season = apps.get_model('rates', 'Season')
        self.location = apps.get_model('rates', 'Location')

    def test_delete_user(self):
        self.user_model.objects.create_user(email='will@gmail.com',
                                            first_name='William',
                                            last_name="Atlas",
                                            preferred_name="Will",
                                            password="super-secret")
        self.client.login(email="will@gmail.com", password="super-secret")
        self.job_title.objects.create(uuid="5c09a673-d0c7-481f-8500-36c581bd7b4e",
                                      title="Camera Operator")
        self.show.objects.create(uuid="48a6f024-2aa1-4f29-8db0-de0454385a2c",
                                 title="Project Runway")
        self.company.objects.create(uuid="0fa1f64b-58d6-4963-914c-b0711c70e051",
                                    name="Magical Elves")
        self.network.objects.create(uuid="a7f641e0-bbfc-4469-9acd-404f2c8b923f",
                                    name="Bravo")
        response = self.client.post(self.add_rate_url, content_type="application/json",
                                    data=valid_json)
        self.assertEqual(response.status_code, 201)
        all_raw_reports = self.raw_rate_report.objects.all()
        self.assertEqual(len(all_raw_reports), 1)
        all_reports = self.rate_report.objects.all()
        self.assertEqual(len(all_reports), 1)

        response = self.client.post(self.settings_url, data={"delete_field": "DELETE"})
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertIn("Your account has been deleted.", response.rendered_content)

        all_raw_reports = self.raw_rate_report.objects.all()
        self.assertEqual(len(all_raw_reports), 0)
        all_reports = self.rate_report.objects.all()
        self.assertEqual(len(all_reports), 1)

        self.assertRaises(self.user_model.DoesNotExist, self.user_model.objects.get,
                          email="will@gmail.com")

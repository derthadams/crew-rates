import json
import uuid

from django.test import TestCase
from django.urls import reverse
from django.apps import apps


class APIViewsTest(TestCase):

    def setUp(self):
        self.job_title = apps.get_model('rates', 'JobTitle')
        self.show = apps.get_model('rates', 'Show')
        self.company = apps.get_model('rates', 'Company')
        self.network = apps.get_model('rates', 'Network')
        self.job_title_url = reverse('job-titles')
        self.show_url = reverse('shows')
        self.company_url = reverse('companies')
        self.network_url = reverse('networks')
        self.autocomplete_url = reverse('autocomplete')
        self.details_url = reverse('details')
        self.sessiontoken = uuid.uuid4()

    def test_no_job_titles(self):
        response = self.client.get(self.job_title_url + '?q=camera')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 0)

    def test_one_job_title(self):
        self.job_title.objects.get_or_create(title='camera operator')
        url = reverse('job-titles')
        response = self.client.get(self.job_title_url + '?q=camera')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 1)

    def test_two_job_titles(self):
        self.job_title.objects.get_or_create(title='camera operator')
        self.job_title.objects.get_or_create(title='camera assistant')
        url = reverse('job-titles')
        response = self.client.get(self.job_title_url + '?q=camera')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 2)

    def test_job_titles_no_match(self):
        self.job_title.objects.get_or_create(title='director of photography')
        self.job_title.objects.get_or_create(title='steadicam operator')
        url = reverse('job-titles')
        response = self.client.get(self.job_title_url + '?q=camera')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 0)

    def test_no_shows(self):
        response = self.client.get(self.show_url + '?q=housewives')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 0)

    def test_one_show(self):
        self.show.objects.get_or_create(title='Real Housewives of Beverly Hills')
        response = self.client.get(self.show_url + '?q=housewives')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 1)

    def test_two_shows(self):
        self.show.objects.get_or_create(title='Real Housewives of New Jersey')
        self.show.objects.get_or_create(title='Real Housewives of Atlanta')
        response = self.client.get(self.show_url + '?q=housewives')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data['results']), 2)

    def test_shows_no_match(self):
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
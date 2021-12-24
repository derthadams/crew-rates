from django.apps import apps
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse


class TestFlatpages(TestCase):
    def setUp(self):
        self.flatpage = apps.get_model('flatpages', 'Flatpage')

    def test_tos(self):
        site = Site.objects.all()[0]
        tos = self.flatpage.objects.create(title='Terms of Service', content='<p>Hey!</p>',
                                           url='/tos/')
        tos.sites.add(site)
        response = self.client.get(reverse('tos'))
        self.assertContains(response, 'Terms of Service')

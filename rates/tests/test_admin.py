import os

from django.test import TestCase
from django.urls import reverse
from django.apps import apps

from rates.admin import RatesInvitationAdminAddForm, calc_percent_increase  # noqa

from .sample_data import valid_json, valid_json_create, valid_json_no_locations


class RatesAdminTest(TestCase):

    def setUp(self):
        self.user_model = apps.get_model('rates', 'User')
        self.job_title = apps.get_model('rates', 'JobTitle') # noqa
        self.show = apps.get_model('rates', 'Show')
        self.company = apps.get_model('rates', 'Company')
        self.network = apps.get_model('rates', 'Network')
        self.season = apps.get_model('rates', 'Season')
        self.location = apps.get_model('rates', 'Location')
        self.raw_rate_report = apps.get_model('rates', 'RawRateReport')
        self.rate_report = apps.get_model('rates', 'RateReport')
        self.rates_invitation = apps.get_model('rates', 'RatesInvitation')
        self.super_user = self.user_model.objects.create_superuser('admin@example.com', 'incredible_secret')
        self.add_rate_url = reverse('add-rate-api')

    def test_add_rates_invitation(self):
        self.client.login(email='admin@example.com', password='incredible_secret')
        admin_path = os.environ.get('ADMIN_PATH')
        response = self.client.post(f'/{admin_path}rates/ratesinvitation/add/',
                         {
                             'email': 'derth@me.com',
                             'name': 'Betty',
                             'inviter': self.super_user.pk
                         },)
        self.assertEqual(response.status_code, 302)
        invitations = self.rates_invitation.objects.all()
        self.assertEqual(len(invitations), 1)

    def test_approve_raw_rate_report_valid_no_create(self):
        self.client.login(email='admin@example.com', password='incredible_secret')
        self.job_title.objects.create(uuid='5c09a673-d0c7-481f-8500-36c581bd7b4e',
                                      title='Camera Operator')
        self.show.objects.create(uuid='48a6f024-2aa1-4f29-8db0-de0454385a2c',
                                 title='Project Runway')
        self.company.objects.create(uuid="0fa1f64b-58d6-4963-914c-b0711c70e051",
                                    name="Magical Elves")
        self.network.objects.create(uuid='a7f641e0-bbfc-4469-9acd-404f2c8b923f',
                                    name="Bravo")
        response = self.client.post(self.add_rate_url, content_type="application/json",
                                    data=valid_json)
        self.assertEqual(response.status_code, 201)
        report = self.raw_rate_report.objects.all()[0]
        data = {'action': 'approve_raw_rate_report', '_selected_action': report.pk}
        change_url = reverse('admin:rates_rawratereport_changelist')
        response = self.client.post(change_url, data)
        self.assertEqual(response.status_code, 302)
        seasons = self.season.objects.all()
        self.assertEqual(len(seasons), 1)
        locations = self.location.objects.all()
        self.assertEqual(len(locations), 4)

    def test_approve_raw_rate_report_valid_create(self):
        self.client.login(email='admin@example.com', password='incredible_secret')
        response = self.client.post(self.add_rate_url, content_type="application/json",
                                    data=valid_json_create)
        self.assertEqual(response.status_code, 201)
        report = self.raw_rate_report.objects.all()[0]
        data = {'action': 'approve_raw_rate_report', '_selected_action': report.pk}
        change_url = reverse('admin:rates_rawratereport_changelist')
        response = self.client.post(change_url, data)
        self.assertEqual(response.status_code, 302)
        seasons = self.season.objects.all()
        self.assertEqual(len(seasons), 1)
        job_titles = self.job_title.objects.all()
        self.assertEqual(len(job_titles), 1)
        self.assertEqual(job_titles[0].title, "Camera Operator")
        shows = self.show.objects.all()
        self.assertEqual(len(shows), 1)
        self.assertEqual(shows[0].title, "Project Runway")
        companies = self.company.objects.all()
        self.assertEqual(len(companies), 1)
        self.assertEqual(companies[0].name, "Magical Elves")
        networks = self.network.objects.all()
        self.assertEqual(len(networks), 1)
        self.assertEqual(networks[0].name, "Bravo")
        locations = self.location.objects.all()
        self.assertEqual(len(locations), 4)

    def test_approve_raw_rate_report_valid_no_locations(self):
        self.client.login(email='admin@example.com', password='incredible_secret')
        response = self.client.post(self.add_rate_url, content_type="application/json",
                                    data=valid_json_no_locations)
        self.assertEqual(response.status_code, 201)
        report = self.raw_rate_report.objects.all()[0]
        data = {'action': 'approve_raw_rate_report', '_selected_action': report.pk}
        change_url = reverse('admin:rates_rawratereport_changelist')
        response = self.client.post(change_url, data)
        self.assertEqual(response.status_code, 302)
        locations = self.location.objects.all()
        self.assertEqual(len(locations), 0)

    def test_approve_raw_rate_report_preexisting_season(self):
        self.client.login(email='admin@example.com', password='incredible_secret')
        job = self.job_title.objects.create(uuid='5c09a673-d0c7-481f-8500-36c581bd7b4e',
                                            title='Camera Operator')
        show = self.show.objects.create(uuid='48a6f024-2aa1-4f29-8db0-de0454385a2c',
                                        title='Project Runway')
        company = self.company.objects.create(uuid="0fa1f64b-58d6-4963-914c-b0711c70e051",
                                              name="Magical Elves")
        network = self.network.objects.create(uuid='a7f641e0-bbfc-4469-9acd-404f2c8b923f',
                                              name="Bravo")
        season = self.season.objects.create(title="Project Runway S4",
                                            show=show,
                                            number=4,)
        season.companies.add(company)
        response = self.client.post(self.add_rate_url, content_type="application/json",
                                    data=valid_json)
        self.assertEqual(response.status_code, 201)
        report = self.raw_rate_report.objects.all()[0]
        data = {'action': 'approve_raw_rate_report', '_selected_action': report.pk}
        change_url = reverse('admin:rates_rawratereport_changelist')
        response = self.client.post(change_url, data)
        self.assertEqual(response.status_code, 302)
        seasons = self.season.objects.all()
        self.assertEqual(len(seasons), 1)
        locations = self.location.objects.all()
        self.assertEqual(len(locations), 4)

    def test_calculate_increase_better_hourly_and_daily(self):
        offered_hourly = 54.5454
        offered_daily = 600
        final_hourly = 60
        final_daily = 660
        increase = calc_percent_increase(final_hourly, final_daily, offered_hourly, offered_daily)
        self.assertEqual(increase, 10)

    def test_calculate_increase_better_hourly_worse_daily(self):
        offered_hourly = 54.5454
        offered_daily = 600
        final_hourly = 60
        final_daily = 480
        increase = calc_percent_increase(final_hourly, final_daily, offered_hourly, offered_daily)
        self.assertIsNone(increase)

    def test_calculate_increase_worse_hourly_better_daily(self):
        offered_hourly = 54.5454
        offered_daily = 600
        final_hourly = 44.64
        final_daily = 625
        increase = calc_percent_increase(final_hourly, final_daily, offered_hourly, offered_daily)
        self.assertIsNone(increase)

    def test_calculate_increase_same_rate(self):
        offered_hourly = 80
        offered_daily = 880
        final_hourly = 80
        final_daily = 880
        increase = calc_percent_increase(final_hourly, final_daily, offered_hourly, offered_daily)
        self.assertIsNone(increase)

    def test_calculate_increase_worse_hourly_worse_daily(self):
        offered_hourly = 60
        offered_daily = 660
        final_hourly = 54.5454
        final_daily = 600
        increase = calc_percent_increase(final_hourly, final_daily, offered_hourly, offered_daily)
        self.assertIsNone(increase)

    def test_approve_raw_rate_report_valid_create_overrides(self):
        self.client.login(email='admin@example.com', password='incredible_secret') # noqa
        assistant = self.job_title.objects.create(uuid='4d932df0-9efa-4996-a4c8-b02d0e9219b7',
                                                  title='Camera Assistant')
        wipeout = self.show.objects.create(uuid='4a72cfed-5ad9-4200-964c-0e62f77882b7', # noqa
                                           title='Wipeout')
        endemol = self.company.objects.create(uuid='caf6966d-a961-4a57-8872-39a4f51ce798',
                                              name='EndemolShine NorthAmerica')
        tbs = self.network.objects.create(uuid='5609fa2a-789e-43e0-80d9-d3cb6e77aed8',
                                          name='TBS')
        response = self.client.post(self.add_rate_url, content_type="application/json", # noqa
                                    data=valid_json_create) # noqa
        self.assertEqual(response.status_code, 201)
        report = self.raw_rate_report.objects.all()[0]
        report.job_title_override = assistant
        report.show_override = wipeout
        report.companies_override.add(endemol)
        report.network_override = tbs
        report.save()
        data = {'action': 'approve_raw_rate_report', '_selected_action': report.pk} # noqa
        change_url = reverse('admin:rates_rawratereport_changelist')
        response = self.client.post(change_url, data)
        self.assertEqual(response.status_code, 302)
        seasons = self.season.objects.all()
        self.assertEqual(len(seasons), 1)
        locations = self.location.objects.all()
        self.assertEqual(len(locations), 4)
        reports = self.rate_report.objects.all()
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0].job_title.pk, assistant.pk)
        self.assertEqual(seasons[0].show.pk, wipeout.pk)
        company_pks = list(seasons[0].companies.all().values_list('id', flat=True))
        self.assertEqual(company_pks[0], endemol.pk)
        self.assertEqual(seasons[0].network.pk, tbs.pk)

from django.apps import apps
from django.test import TestCase

from datetime import datetime, timezone, timedelta


class TestModels(TestCase):

    def setUp(self):
        self.user_model = apps.get_model('rates', 'User')
        self.company = apps.get_model('rates', 'Company')
        self.job_title = apps.get_model('rates', 'JobTitle')
        self.show = apps.get_model('rates', 'Show')
        self.network = apps.get_model('rates', 'Network')
        self.location = apps.get_model('rates', 'Location')
        self.season = apps.get_model('rates', 'Season')
        self.raw_rate_report = apps.get_model('rates', 'RawRateReport')
        self.rate_report = apps.get_model('rates', 'RateReport')

    def test_user_model_no_email(self):
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user(email="", password="allmysecrets")

    def test_user_get_absolute_url(self):
        user = self.user_model.objects.create_user(email="john@google.com", password="allmysecrets")
        url = user.get_absolute_url()
        self.assertEquals(url, f"/users/{user.pk}/")

    def test_user_string(self):
        user = self.user_model.objects.create_user(email="john@google.com", password="allmysecrets")
        user_str = str(user)
        self.assertEquals(user_str, "john@google.com")

    def test_company_string(self):
        company = self.company.objects.create(name="Google")
        company_str = str(company)
        self.assertEquals(company_str, "Google")

    def test_job_title_string(self):
        job_title = self.job_title.objects.create(title="Camera Operator")
        job_title_str = str(job_title)
        self.assertEquals(job_title_str, "Camera Operator")

    def test_show_string(self):
        show = self.show.objects.create(title="Vertigo")
        show_str = str(show)
        self.assertEquals(show_str, "Vertigo")

    def test_network_string(self):
        network = self.network.objects.create(name="HBO Max")
        network_str = str(network)
        self.assertEquals(network_str, "HBO Max")

    def test_location_string(self):
        location = self.location.objects.create(display_name="West Hollywood, CA, US")
        location_str = str(location)
        self.assertEquals(location_str, "West Hollywood, CA, US")

    def test_season_string(self):
        show = self.show.objects.create(title="Supermarket Sweep")
        season = self.season.objects.create(show=show, number=1)
        season_str = str(season)
        self.assertEquals(season_str, "Supermarket Sweep (Season 1)")

    def test_raw_rate_report_string(self):
        user = self.user_model.objects.create_user(email="john@google.com", password="allmysecrets")
        job_title = self.job_title.objects.create(title="Camera Operator")
        show = self.show.objects.create(title="Supermarket Sweep")
        report = self.raw_rate_report.objects.create(user=user, job_title=job_title.pk,
                                                     job_title_name="Camera Operator",
                                                     offered_hourly=63.6363, offered_guarantee=10,
                                                     show=show.pk, negotiated=False,
                                                     show_title="Supermarket Sweep",
                                                     season_number=1, start_date="2020-08-07")
        report_str = str(report)
        self.assertEquals(report_str, "john@google.com: Supermarket Sweep S1, Camera Operator, "
                                      "$63.6363")

    def test_rate_report_string(self):
        user = self.user_model.objects.create_user(email="john@google.com", password="allmysecrets")
        show = self.show.objects.create(title="Supermarket Sweep")
        season = self.season.objects.create(show=show, number=1)
        job_title = self.job_title.objects.create(title="Camera Operator")
        report = self.rate_report.objects.create(user=user, job_title=job_title,
                                                 season=season,
                                                 offered_hourly=63.6363, offered_guarantee=10)
        report_str = str(report)
        self.assertEquals(report_str, "john@google.com: Supermarket Sweep (Season 1), "
                                      "Camera Operator, $63.6363")

    def test_created_updated(self):
        job_title = self.job_title.objects.create(title="Camera Operator")
        duration = datetime.now(timezone(-timedelta(hours=8))) - job_title.created_at
        self.assertLessEqual(duration, timedelta(seconds=1))
        job_title.title = "Steadicam Operator"
        self.assertNotEquals(job_title.created_at, job_title.modified_at)
        duration = datetime.now(timezone(-timedelta(hours=8))) - job_title.modified_at
        self.assertLessEqual(duration, timedelta(seconds=1))


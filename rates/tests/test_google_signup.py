import time

from django.apps import apps
from django.contrib.sites.models import Site
from django.core import mail
from django.test import LiveServerTestCase
from django.urls import reverse
from django.utils import timezone

from allauth.socialaccount.models import SocialApp

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .sample_user import google_user
from .config import go


class TestGoogleSignup(LiveServerTestCase):

    @classmethod
    def setUp(cls):
        cls.port = 9010
        super().setUpClass() # noqa

        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        cls.selenium = webdriver.Chrome(chrome_options=chrome_options)
        cls.selenium.implicitly_wait(10)
        cls.invitation_model = apps.get_model('rates', 'RatesInvitation')

        cls.site = Site.objects.get_current()
        cls.site_url = Site.objects.get_current().domain

    def test_google_signup(self):
        google = SocialApp.objects.create(provider=go["provider"],
                                          name=go["name"],
                                          client_id=go["client_id"],
                                          secret=go["secret"])
        google.sites.add(self.site)

        key = "w6fg9sd8f7gasd9f78a6d9gsd7f899fd78g9aa70f9s7d8g999f"

        self.invitation_model.objects.create(first_name=google_user["first_name"], # noqa
                                             last_name=google_user["last_name"],
                                             preferred_name=google_user["preferred_name"],
                                             email=google_user["email"],
                                             key=key, sent=timezone.now())

        invitations = self.invitation_model.objects.all()
        self.assertEqual(len(invitations), 1)

        invite_url = reverse('invitations:accept-invite',
                             kwargs={'key': key})
        self.selenium.get('%s%s' % (self.live_server_url, invite_url))
        self.assertEqual(self.selenium.title, "Signup")

        sign_up_with_go = self.selenium.find_element_by_link_text("Sign up with Google")
        sign_up_with_go.click()

        self.assertIn("Sign in - Google Accounts", self.selenium.title)
        email = self.selenium.find_element_by_id("identifierId")
        email.send_keys(google_user["email"])
        next_button = self.selenium.find_element_by_xpath(
            "//span[contains(text(), 'Next')]/parent::button")
        next_button.click()

        self.assertIn("Welcome", self.selenium.page_source)
        password = self.selenium.find_element_by_name("password")
        password.send_keys(google_user['password'])
        password_next = self.selenium.find_element_by_id("passwordNext")
        password_next.click()

        go_oauth_redirect = self.selenium.current_url
        self.selenium.get("http:" + go_oauth_redirect[6:])

        self.assertIn("Welcome", self.selenium.page_source)

        # if "Welcome" in self.selenium.page_source:
        #     password = self.selenium.find_element_by_name("password")
        #     password.send_keys(google_user['password'])
        #     password_next = self.selenium.find_element_by_id("passwordNext")
        #     password_next.click()
        #
        #     if "Something went wrong" in self.selenium.page_source:
        #         time.sleep(1)
        #         next_button = self.selenium.find_element_by_xpath(
        #             "//button[1]")
        #         next_button.click()  # Leads to 400 error page

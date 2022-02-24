from time import sleep

from django.apps import apps
from django.contrib.sites.models import Site
from django.test import LiveServerTestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.utils import timezone

from allauth.socialaccount.models import SocialApp

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .sample_user import twitter_user
from .config import fb, tw


@override_settings(DEBUG=True)
class TestGoogleSignup(LiveServerTestCase):

    @classmethod
    def setUp(cls):
        cls.port = 9020
        super().setUpClass() # noqa

        chrome_options = Options()
        # chrome_options.add_argument("--headless")

        cls.selenium = webdriver.Chrome(chrome_options=chrome_options)

        cls.selenium.implicitly_wait(10)
        cls.invitation_model = apps.get_model('rates', 'RatesInvitation')

        cls.site = Site.objects.get_current()
        cls.site_url = Site.objects.get_current().domain

    def test_twitter_signup(self):
        twitter = SocialApp.objects.create(provider=tw["provider"],
                                           name=tw["name"],
                                           client_id=tw["client_id"],
                                           secret=tw["secret"])
        twitter.sites.add(self.site)

        facebook = SocialApp.objects.create(provider=fb["provider"],
                                            name=fb["name"],
                                            client_id=fb["client_id"],
                                            secret=fb["secret"])
        facebook.sites.add(self.site)

        key = "w6fg7d9f8gasd9f78a6d9gsd3h6jk99fd78g9aa70fadkflu2"

        self.invitation_model.objects.create(first_name=twitter_user["first_name"], # noqa
                                             last_name=twitter_user["last_name"],
                                             preferred_name=twitter_user["preferred_name"],
                                             email=twitter_user["email"],
                                             key=key, sent=timezone.now())

        invitations = self.invitation_model.objects.all()
        self.assertEqual(len(invitations), 1)

        invite_url = reverse('invitations:accept-invite',
                             kwargs={'key': key})
        self.selenium.get('%s%s' % (self.live_server_url, invite_url))
        self.assertEqual(self.selenium.title, "Signup")

        sign_up_with_tw = self.selenium.find_element_by_link_text("Sign up with Twitter")
        sign_up_with_tw.click()

        self.assertIn("Authorize crewrates.org to access your account?", self.selenium.page_source)
        email = self.selenium.find_element_by_id("username_or_email")
        email.send_keys(twitter_user["email"])

        password = self.selenium.find_element_by_id("password")
        password.send_keys(twitter_user["password"])

        allow = self.selenium.find_element_by_id("allow")
        allow.click()
        sleep(1)

        if not self.selenium.current_url.startswith("https://localhost"):
            email = self.selenium.find_element_by_name("text")
            email.send_keys(twitter_user["email"])
            next_button = self.selenium.find_element_by_xpath(
                "//span[contains(text(), 'Next')]/ancestor::div[@role='button']")
            next_button.click()

            username = self.selenium.find_element_by_name("text")
            username.send_keys(twitter_user["handle"])
            next_button = self.selenium.find_element_by_xpath(
                "//span[contains(text(), 'Next')]/ancestor::div[@role='button']")
            next_button.click()

            password = self.selenium.find_element_by_name("password")
            password.send_keys(twitter_user["password"])

            login = self.selenium.find_element_by_xpath(
                "//span[contains(text(), 'Log in')]/ancestor::div[@role='button']")
            login.click()
            sleep(1)

            if not self.selenium.current_url.startswith("https://localhost"):
                authorize = self.selenium.find_element_by_id("allow")
                authorize.click()

        tw_oauth_redirect = self.selenium.current_url
        self.selenium.get("http:" + tw_oauth_redirect[6:])

        self.assertIn(f"Invitation to - {twitter_user['email']} - has been accepted",
                      self.selenium.page_source)

        self.selenium.get("https://twitter.com/settings/connected_apps")
        sleep(2)

        self.assertIn("crewrates.org", self.selenium.page_source)

        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/password/set/')) # noqa
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys(twitter_user["cr_password"])
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys(twitter_user["cr_password"])
        set_password = self.selenium.find_element_by_xpath(
            "//button[contains(text(), 'Set password')]")
        set_password.click()

        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/social/connections/'))
        remove = self.selenium.find_element_by_class_name('bs-social-btn-delete')
        remove.click()

        self.selenium.get("https://twitter.com/settings/connected_apps")
        sleep(1)
        self.assertIn("You don’t have any connected apps", self.selenium.page_source)

    def tearDown(self):
        self.selenium.quit()

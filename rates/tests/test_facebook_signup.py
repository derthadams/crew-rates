import re

from django.apps import apps
from django.contrib.sites.models import Site
from django.core import mail
from django.test import LiveServerTestCase
from django.urls import reverse
from django.utils import timezone

from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.webdriver import WebDriver
# from selenium.webdriver.common.keys import Keys

from .sample_user import test_user
from .config import fb


class TestFacebookSignup(LiveServerTestCase):

    @classmethod
    def setUp(cls):
        cls.port = 8090
        super().setUpClass()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        cls.selenium = webdriver.Chrome(chrome_options=chrome_options)
        cls.selenium.implicitly_wait(10)
        cls.invitation_model = apps.get_model('rates', 'RatesInvitation')

        cls.site = Site.objects.get_current()
        cls.site_url = Site.objects.get_current().domain

    def test_facebook_signup(self):
        facebook = SocialApp.objects.create(provider=fb["provider"],
                                            name=fb["name"],
                                            client_id=fb["client_id"],
                                            secret=fb["secret"])
        facebook.sites.add(self.site)

        key = "s6fg9sd8f76asd9f78a6d9g76s9fd78g9adaf79sd8f7"
        self.invitation_model.objects.create(first_name=test_user["first_name"],
                                             last_name=test_user["last_name"],
                                             preferred_name=test_user["preferred_name"],
                                             email=test_user["preferred_name"],
                                             key=key, sent=timezone.now())

        invitations = self.invitation_model.objects.all()
        self.assertEqual(len(invitations), 1)

        invite_url = reverse('invitations:accept-invite',
                             kwargs={'key': key})
        self.selenium.get('%s%s' % (self.live_server_url, invite_url))
        self.assertEqual(self.selenium.title, "Signup")

        sign_up_with_fb = self.selenium.find_element_by_link_text("Sign up with Facebook")
        sign_up_with_fb.click()

        self.assertIn("Log into Facebook", self.selenium.title)
        email = self.selenium.find_element_by_id("email")
        email.send_keys(test_user["email"])

        password = self.selenium.find_element_by_id("pass")
        password.send_keys(test_user["password"])

        self.assertIn("Log Into Facebook", self.selenium.page_source)

        login_button = self.selenium.find_element_by_id("loginbutton")
        login_button.click()

        self.assertIn("Log in with Facebook", self.selenium.title)

        edit_access = self.selenium.find_element_by_xpath("//*[contains(text(), 'Edit access')]")
        edit_access.click()

        email_switch = self.selenium.find_element_by_css_selector('[aria-label="email"]')
        continue_as = self.selenium.find_element_by_css_selector('[aria-label="Continue as Ruth"]')
        continue_as.click()

        fb_oauth_redirect = self.selenium.current_url

        self.selenium.get("http:" + fb_oauth_redirect[6:])

        self.selenium.get("https://www.facebook.com/settings?tab=applications&ref=settings")
        self.assertIn("crewrates.org", self.selenium.page_source)

        self.assertEqual(len(mail.outbox), 1)
        confirmation_url = re.search("(https).*", mail.outbox[0].body).group(0)
        confirmation_url = "http:" + confirmation_url[6:]

        self.selenium.get(confirmation_url)
        confirm = self.selenium.find_element_by_xpath("//button[contains(text(), 'Confirm')]")
        confirm.click()

        sign_in_with_fb = self.selenium.find_element_by_link_text("Sign in with Facebook")
        sign_in_with_fb.click()

        fb_oauth_redirect = self.selenium.current_url
        self.selenium.get("http:" + fb_oauth_redirect[6:])

        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/password/set/'))
        password1 = self.selenium.find_element_by_id("id_password1")
        password1.send_keys(test_user["cr_password"])
        password2 = self.selenium.find_element_by_id("id_password2")
        password2.send_keys(test_user["cr_password"])
        set_password = self.selenium.find_element_by_xpath("//button[contains(text(), 'Set password')]")
        set_password.click()

        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/social/connections/'))
        remove = self.selenium.find_element_by_class_name('bs-social-btn-delete')
        remove.click()

        self.selenium.get("https://www.facebook.com/settings?tab=applications&ref=settings")
        self.assertIn("You don't have any apps or websites to review", self.selenium.page_source)

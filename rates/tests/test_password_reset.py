from django.test import TestCase
from django.urls import reverse
from rates.forms import RatesResetPasswordForm # noqa
from rates.models import User # noqa


class TestResetPassword(TestCase):
    def test_reset_password(self):
        User.objects.create(email='will.atlas@gmail.com', first_name='Will', last_name='Atlas')
        response = self.client.post(reverse('account_reset_password'),
                                    data={'email': 'will.atlas@gmail.com'})
        self.assertEqual(response.status_code, 302)

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from crew_rates.settings.base import get_env_variable # noqa


class TestGetEnvVariable(TestCase):
    def test_error(self):
        with self.assertRaises(ImproperlyConfigured):
            get_env_variable('DOES_NOT_EXIST')
        # self.assertTrue('Set the DOES_NOT_EXIST environment variable' in context.exception)

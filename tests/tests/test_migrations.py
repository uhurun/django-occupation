import unittest

from django.apps import apps
from django.db import ProgrammingError
from django.test import TestCase

from occupation.utils import enable_row_level_security, disable_row_level_security


class TestMigrationOperations(TestCase):
    def test_enable_disable_rls(self):
        enable_row_level_security('tests', 'AwareModel', apps)
        disable_row_level_security('tests', 'AwareModel', apps)

    def test_enable_fails_if_no_fk_to_tenant(self):
        with self.assertRaises(Exception) as exc:
            enable_row_level_security('tests', 'NaiveModel', apps)
            self.assertEqual('Unable to find any FK chains back to tenant model.', exc.message)

    def test_disable_fails_when_rls_not_enabled(self):
        with self.assertRaises(ProgrammingError):
            disable_row_level_security('tests', 'AwareModel', apps)

    @unittest.expectedFailure
    def test_enable_rls_with_superuser_policy(self):
        enable_row_level_security('tests', 'AwareModel', apps, superuser=True)
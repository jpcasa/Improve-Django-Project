from . import settings
from . import wsgi
from django.test import TestCase


class TestDebugToolbar(TestCase):
    def test_debug_toolbar(self):
        self.assertTrue(settings.show_debug_toolbar(''))

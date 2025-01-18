import unittest

from db.dao import *


class TestDao(unittest.TestCase):
    def test_list_alert(self):
        list = filter_alert(None, None, None)
        self.assertTrue(len(list))

    def test_list_stat(self):
        list = filter_stat(None, None, None)
        self.assertTrue(len(list))

    def test_add_alert(self):
        try:
            add_alert("WARNING", "Образовалась пробка")
        except Exception:
            raise

    def test_add_stat(self):
        try:
            add_stat("car", 5)
        except Exception:
            raise

# Test Routes
import unittest
from app import create_app

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

from django.test import TestCase
from utils.apihelper import APIHelper

import requests
import os


class APIHelperTests(TestCase):
    def setUp(self):
        self.url = 'https://reqres.in/api/users'

    def test_can_read_api_key(self):
        """Test that api key is read from env file"""
        api_key = os.environ.get('YOUTUBE_API_KEY')
        self.assertIsNotNone(api_key)

    def test_apihelper_returns_valid_json(self):
        """Test that api helper returns valid json dictionary"""
        api_helper = APIHelper(self.url)
        response = requests.get(self.url)

        self.assertEqual(api_helper.response.status_code, 200)
        self.assertEqual(response.json(), api_helper.getJSONAsDict())

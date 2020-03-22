from django.test import TestCase
from django.conf import settings
from utils.csvwriter import CSVWriter

import os


class CSVWriterTests(TestCase):
    def setUp(self):
        self.file_name = os.path.join(settings.MEDIA_ROOT, 'test.csv')

    def test_csvwriter_creates_file(self):
        headers = ['id', 'email', 'name']
        data = [
            {
                'id': 7,
                'email': 'michael.lawson@reqres.in',
                'name': 'Michael'
            },
            {
                'id': 8,
                'email': 'lindsay.ferguson@reqres.in',
                'name': 'Lindsay'
            }
        ]
        csv_writer = CSVWriter(self.file_name, headers)
        csv_writer.write(data)

        self.assertTrue(os.path.exists(self.file_name))

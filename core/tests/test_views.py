from django.test import TestCase, Client
from django.urls import reverse


INDEX_URL = reverse('core:home')


class ViewTests(TestCase):
    def setUp(self):
        """Setup test client"""
        self.client = Client()

    def test_get_request(self):
        """Test default page is successfully recieved"""
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_url(self):
        """Test invalid url message is provided to template"""
        payload = {
            'url': 'http://example.com'
        }

        response = self.client.post(INDEX_URL, data=payload)
        messages = [m.message for m in response.context['messages']]

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('file_name', response.context.keys())
        self.assertIn('Not an Amazon product link or a YouTube video link', messages)
        self.assertEqual(len(messages), 1)

    def test_post_amazon_url(self):
        """Test response to valid amazon product url"""
        payload = {
            'url': 'https://www.amazon.com/dp/B00SI0MCL4/'
        }
        file_name = 'reviews-B00SI0MCL4.csv'

        response = self.client.post(INDEX_URL, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['file_name'], file_name)

    def test_post_youtube_url(self):
        """Test response to valid youtube video url"""
        payload = {
            'url': 'https://www.youtube.com/watch?v=BjZbAzUM9Ao'
        }
        file_name = 'comments-BjZbAzUM9Ao.csv'

        response = self.client.post(INDEX_URL, data=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['file_name'], file_name)

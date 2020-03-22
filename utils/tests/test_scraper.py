from django.test import TestCase
from utils.scraper import Scraper


class ScraperTests(TestCase):
    def setUp(self):
        self.url = 'https://www.amazon.com/dp/B00SI0MCL4/'

    def test_scraper_returns_no_error(self):
        scraper = Scraper(self.url)
        response = scraper.getReviewsAsDict()

        self.assertNotIn('error', response)

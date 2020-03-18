from lxml import html
from dateutil import parser as dateparser

import requests
import json
import re


class Scraper():
    def __init__(self, url):
        self.url = url

    def getHTML(self):
        # Add some recent user agent to prevent amazon from blocking the request
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
        response = requests.get(self.url, headers=headers, verify=False, timeout=30)

        # Removing the null bytes from the response.
        cleaned_response = response.text.replace('\x00', '')
        parser = html.fromstring(cleaned_response)

        return response, parser

    def getReviewsAsDict(self):
        response, parser = self.getHTML()

        if response.status_code == 404:
            return {"url": self.url, "error": "page not found"}
        if response.status_code != 200:
            return {"url": self.url, "error": "failed to process the page"}

        XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
        XPATH_PRODUCT_PRICE = '//span[@id="priceblock_ourprice"]/text()'
        XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
        XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'

        raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
        raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)
        reviews = parser.xpath(XPATH_REVIEW_SECTION_1)

        product_price = ''.join(raw_product_price).replace(',', '')
        product_name = ''.join(raw_product_name).strip()

        if not reviews:
            reviews = parser.xpath(XPATH_REVIEW_SECTION_2)

        reviews_list = []

        # Parsing individual reviews
        for review in reviews:
            XPATH_AUTHOR = './/span[contains(@class,"profile-name")]//text()'
            XPATH_RATING = './/i[@data-hook="review-star-rating"]//text()'
            XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
            XPATH_REVIEW_LINK = './/a[@data-hook="review-title"]/@href'
            XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
            XPATH_REVIEW_TEXT_1 = './/div[@data-hook="review-collapsed"]//text()'
            XPATH_REVIEW_TEXT_2 = './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview'
            XPATH_REVIEW_TEXT_3 = './/div[contains(@id,"dpReviews")]/div/text()'

            raw_review_author = review.xpath(XPATH_AUTHOR)
            raw_review_rating = review.xpath(XPATH_RATING)
            raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
            raw_review_link = review.xpath(XPATH_REVIEW_LINK)
            raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
            raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
            raw_review_text2 = review.xpath(XPATH_REVIEW_TEXT_2)
            raw_review_text3 = review.xpath(XPATH_REVIEW_TEXT_3)

            # Cleaning data
            author = ' '.join(' '.join(raw_review_author).split())
            review_rating = ''.join(raw_review_rating).replace('out of 5 stars', '')
            review_header = ' '.join(' '.join(raw_review_header).split())
            review_link = ''.join(' '.join(raw_review_link).split())

            try:
                review_posted_date = dateparser.parse(''.join(raw_review_posted_date[0].split()[-3:])).strftime('%d %b %Y')
            except ValueError:
                review_posted_date = None

            review_text = ' '.join(' '.join(raw_review_text1).split())

            # Grabbing hidden comments if present
            if raw_review_text2:
                json_loaded_review_data = json.loads(raw_review_text2[0])
                json_loaded_review_data_text = json_loaded_review_data['rest']
                cleaned_json_loaded_review_data_text = re.sub('<.*?>', '', json_loaded_review_data_text)
                full_review_text = review_text+cleaned_json_loaded_review_data_text
            else:
                full_review_text = review_text

            if not raw_review_text1:
                full_review_text = ' '.join(' '.join(raw_review_text3).split())

            review_dict = {
                'review_text': full_review_text,
                'review_posted_date': review_posted_date,
                'review_header': review_header,
                'review_link': review_link,
                'review_rating': review_rating,
                'review_author': author
            }
            reviews_list.append(review_dict)

        data = {
            'reviews': reviews_list,
            'url': self.url,
            'name': product_name,
            'price': product_price
        }

        return data

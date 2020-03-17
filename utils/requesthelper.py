import os
import re

from enum import Enum
from utils.apihelper import APIHelper


class URLType(Enum):
    AMAZON = 0
    YOUTUBE = 1


class RequestHelper():
    def __init__(self, url):
        self.url = url
        self.url_type = self.getURLType()

        self.api_helper = None
        self.YOUTUBE_COMMENTS_API = 'https://www.googleapis.com/youtube/v3/commentThreads'

    def configureAPIHelper(self, url, payload=None):
        self.api_helper = APIHelper(url, payload)

    def getURLType(self):
        amazon_pattern = re.compile(
            r'^https?:\/\/(?=(?:....)?amazon|smile)(www|smile)\S+com(((?:\/(?:dp|gp)\/([A-Z0-9]+))?\S*[?&]?(?:tag=))?\S*?)(?:#)?(\w*?-\w{2})?(\S*)(#?\S*)+')
        youtube_pattern = re.compile(
            r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?')

        if amazon_pattern.match(self.url):
            return URLType.AMAZON
        elif youtube_pattern.match(self.url):
            return URLType.YOUTUBE

        return None

    def getResult(self, next_page_token=None):
        result = {}

        if self.url_type is URLType.AMAZON:
            result = self.getAmazonReviews()
        elif self.url_type is URLType.YOUTUBE:
            result = self.getYouTubeComments(next_page_token)

        return result

    def getAmazonReviews(self):
        package = {}

        return package

    def getYouTubeComments(self, next_page_token):
        package = {}

        video_id = self.url.split('?v=')[1]
        api_key = os.environ.get('YOUTUBE_API_KEY')

        assert api_key is not None, 'Could not read YouTube API Key, YOUTUBE_API_KEY'

        payload = {
            'part': 'snippet, replies',
            'videoId': video_id,
            'key': api_key
        }

        if next_page_token:
            payload['pageToken'] = next_page_token

        self.configureAPIHelper(self.YOUTUBE_COMMENTS_API, payload=payload)
        package = self.api_helper.getJSONAsDict()

        return package

import requests


class APIHelper():
    def __init__(self, url, payload=None):
        self.url = url
        self.response = requests.get(url, params=payload)

    def getJSONAsDict(self):
        assert self.response.status_code == requests.codes.ok, 'GET {} {}'.format(
            self.url, self.response.status_code)

        return self.response.json()

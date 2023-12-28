import json
import requests
import urllib


# TODO: The client needs the requests package: pip3 install requests
class TestAPIClient:

    DEFAULT_BASE_URL = 'http://localhost:8080/'
    DEFAULT_API_URI = '/api/ui/'

    def __init__(self, base_url=None, api_uri=None):
        self.base_url = base_url if base_url else self.DEFAULT_BASE_URL
        self.api_uri = api_uri if api_uri else self.DEFAULT_API_URI
        self.response = None

    def send(self, json_data):
        connection_url = urllib.parse.urljoin(self.base_url, self.api_uri)
        self.response = requests.post(
            connection_url,
            json=json_data
        )


if __name__ == '__main__':
    sample_data = {'test': 'JSON'}
    client = TestAPIClient()
    client.send(
        json.dumps(sample_data)
    )
    print(client.response.json())

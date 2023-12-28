import json
from socket import error as socket_error
import requests
from unittest import TestCase
from unittest.mock import patch, MagicMock
import urllib

from http_server import _call_ws_server
from constants import C_HTTP_SERVER_PORT


class TestHTTPServer(TestCase):

    def setUp(self):
        base_url = f'http://localhost:{C_HTTP_SERVER_PORT}'
        post_api_uri = '/api/ui'
        self.api_url = urllib.parse.urljoin(base_url, post_api_uri)
        self.sample_data = {'test': 'JSON'}

    def test_get_not_implemented(self):
        response = requests.get(self.api_url)
        assert response.status_code == 501

    def test_post_invalid_json_data(self):
        response = requests.post(self.api_url, json=None)
        assert response.status_code == 400

    @patch('http_server._call_ws_server')
    def test_post_valid_json_no_ws_server_connection(self, mocked_ws_call):
        mocked_ws_call.return_value = None
        response = requests.post(self.api_url,
                                 json=json.dumps(self.sample_data)
                                 )
        assert response.status_code == 503

    @patch('http_server._call_ws_server')
    def test_post_valid_json_ws_server_connection_up(self, mocked_ws_call):
        mocked_ws_call.return_value = json.dumps(self.sample_data)
        response = requests.post(self.api_url,
                                 json.dumps(self.sample_data)
                                 )
        print('response: ', response)
        assert response.status_code == 200


class TestWSClient(TestCase):

    def setUp(self):
        self.sample_json_data = json.dumps({'test': 'JSON'})

    @patch('http_server.ws_connect')
    def test_no_ws_server_up(self, mocked_ws_connect):
        mocked_ws_connect.side_effect = socket_error('test_socket_error')
        response = _call_ws_server(self.sample_json_data)
        assert response is None

    @patch('http_server.ws_connect')
    def test_get_value_from_ws_server(self, mocked_ws_connect):
        mocked_ws_connect.return_value.recv.return_value = self.sample_json_data
        response = _call_ws_server(self.sample_json_data)
        assert response == self.sample_json_data

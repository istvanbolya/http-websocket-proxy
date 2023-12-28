import json
from socket import error as socket_error
from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase

from proxy.tools import _call_ws_server


class WSClientTests(SimpleTestCase):

    def setUp(self):
        self.sample_json_data = json.dumps({'test': 'JSON'})

    @patch('proxy.tools.ws_connect')
    def test_no_ws_server_up(self, mocked_ws_connect):
        mocked_ws_connect.side_effect = socket_error('test_socket_error')
        response = _call_ws_server(self.sample_json_data)
        assert response is None

    @patch('proxy.tools.ws_connect')
    def test_get_value_from_ws_server(self, mocked_ws_connect):
        mocked_ws_connect.return_value.recv.return_value = self.sample_json_data
        response = _call_ws_server(self.sample_json_data)
        assert response == self.sample_json_data

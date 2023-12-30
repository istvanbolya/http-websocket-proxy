import json
from unittest.mock import patch, MagicMock

from django.test import SimpleTestCase, Client, override_settings


class ProxyViewTest(SimpleTestCase):

    def setUp(self):
        self.api_client = Client()
        self.sample_data = {'test': 'JSON'}

    def test_get_not_implemented(self):
        response = self.api_client.get('/api/ui/')
        assert response.status_code == 501

    def test_post_invalid_json(self):
        response = self.api_client.post('/api/ui/')
        assert response.status_code == 400

    @patch('proxy.views._call_ws_server')
    def test_post_valid_json_no_ws_server_connection(self, mocked_ws_call):
        mocked_ws_call.return_value = None
        response = self.api_client.post('/api/ui/',
                                        json.dumps(self.sample_data),
                                        content_type="application/json")
        assert response.status_code == 503

    @patch('proxy.views._call_ws_server')
    def test_post_valid_json_ws_server_connection_up(self, mocked_ws_call):
        mocked_ws_call.return_value = json.dumps(self.sample_data)
        response = self.api_client.post('/api/ui/',
                                        json.dumps(self.sample_data),
                                        content_type="application/json")
        assert response.status_code == 200

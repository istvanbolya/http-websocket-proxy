import json
from socket import error as socket_error
from unittest.mock import patch, MagicMock

from flask_server import app, _call_ws_server
from constants import C_API_POST_URI


TEST_DATA = {'test': 'JSON'}

# === API ===
def test_api_get_not_implemented():
    res = app.test_client().get(C_API_POST_URI)
    assert res.status_code == 501


def test_api_post_invalid_json():
    res = app.test_client().post(C_API_POST_URI, json=None)
    assert res.status_code == 400


@patch('flask_server._call_ws_server')
def test_api_post_valid_json_no_ws_server(mocked_ws_server_call):
    mocked_ws_server_call.return_value = None
    res = app.test_client().post(C_API_POST_URI, json=TEST_DATA)
    assert res.status_code == 503


@patch('flask_server._call_ws_server')
def test_api_post_valid_json_ws_server_up(mocked_ws_server_call):
    mocked_ws_server_call.return_value = json.dumps(TEST_DATA)
    res = app.test_client().post(C_API_POST_URI, json=TEST_DATA)
    assert res.status_code == 200


# === WS Client ===
@patch('flask_server.ws_connect')
def test_no_ws_server(mocked_ws_connect):
    mocked_ws_connect.side_effect = socket_error('test_socket_error')
    response = _call_ws_server(json.dumps(TEST_DATA))
    assert response is None


@patch('flask_server.ws_connect')
def test_get_value_from_ws_server(mocked_ws_connect):
    mocked_ws_connect.return_value.recv.return_value = json.dumps(TEST_DATA)
    response = _call_ws_server(json.dumps(TEST_DATA))
    assert response == json.dumps(TEST_DATA)

from flask import Flask, request, Response
import logging
import json
import sys
from socket import error as socket_error
import urllib.parse
from websockets.sync.client import connect as ws_connect

from constants import C_API_POST_URI, C_HTTP_SERVER_PORT, C_WEBSOCKET_SERVER_BASE_URL, C_WEBSOCKET_ECHO_URI

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout
)

app = Flask(__name__)


def _call_ws_server(json_data):
    ws_server_url = urllib.parse.urljoin(C_WEBSOCKET_SERVER_BASE_URL, C_WEBSOCKET_ECHO_URI)
    try:
        ws_connection = ws_connect(ws_server_url)
        logging.info(f'Connected to WS server: "{ws_server_url}"')
    except socket_error:
        logging.error(f'Cannot connect to WS server: "{ws_server_url}"')
        return
    ws_connection.send(json_data)
    response = ws_connection.recv()
    logging.info(f'Received from WS server: "{response}"')
    ws_connection.close()
    return response

@app.post(C_API_POST_URI)
def handle_post():
    json_data = request.get_data()
    try:
        parsed_data = json.loads(json_data)
        logging.info(f'parsed_data: {parsed_data}')
    except json.decoder.JSONDecodeError:
        error_msg = 'Invalid JSON data'
        logging.error(error_msg)
        return Response(
            error_msg,
            status=400,
        )
    ws_response = _call_ws_server(json_data)
    if not ws_response:
        return Response(
            'Cannot connect to WS server!',
            status=503
        )
    return Response(
        ws_response,
        status=200
    )

@app.get(C_API_POST_URI)
def handle_get():
    return Response(
        'Not implemented',
        status=501,
    )

if __name__ == '__main__':
    app.run(
        debug=True,
        port=C_HTTP_SERVER_PORT
    )

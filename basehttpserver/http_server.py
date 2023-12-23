import json
import logging
import re
import sys
import urllib.parse
from websockets.sync.client import connect as ws_connect

from http.server import BaseHTTPRequestHandler, HTTPServer

from constants import C_API_POST_URI_REGEX, C_HTTP_SERVER_PORT, C_WEBSOCKET_SERVER_BASE_URL, C_WEBSOCKET_ECHO_URI

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    stream=sys.stdout
)

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def _call_ws_server(self, json_data):
        ws_server_url = urllib.parse.urljoin(C_WEBSOCKET_SERVER_BASE_URL, C_WEBSOCKET_ECHO_URI)
        with ws_connect(ws_server_url) as websocket:
            logging.info(f'Connected to WS server: "{ws_server_url}"')
            websocket.send(json_data)
            response = websocket.recv()
            logging.info(f'Received from WS server: "{response}"')
        return response

    def do_POST(self):
        if not re.search(C_API_POST_URI_REGEX, self.path):
            self.send_response(400)
            self.end_headers()
            return
        content_length = int(self.headers.get('content-length'))
        json_data = self.rfile.read(content_length)
        try:
            parsed_data = json.loads(json_data)
            logging.info(f'Received data : "{parsed_data}"')
        except json.decoder.JSONDecodeError:
            logging.error('Invalid JSON Data!')
            self.send_response(400)
            self.end_headers()
            return
        response = self._call_ws_server(json_data)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response)

    def do_GET(self):
        logging.info('Not Implemented!')
        self.send_response(501)
        self.end_headers()


if __name__ == '__main__':
    server = HTTPServer(('localhost', C_HTTP_SERVER_PORT), HTTPRequestHandler)
    logging.info('Starting httpd...\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    logging.info('Stopping httpd...\n')
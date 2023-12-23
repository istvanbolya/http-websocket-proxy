import json
import logging
import urllib
from socket import error as socket_error
from websockets.sync.client import connect as ws_connect

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View

logger = logging.getLogger(__name__)


class ProxyView(View):

    def _call_ws_server(self, json_data):
        ws_server_url = urllib.parse.urljoin(
            settings.WEBSOCKET_SERVER_BASE_URL,
            settings.WEBSOCKET_ECHO_URI
        )
        try:
            ws_connection = ws_connect(ws_server_url)
            logger.debug(f'Connected to WS server: "{ws_server_url}"')
        except socket_error:
            logger.error(f'Cannot connect to WS server: "{ws_server_url}"')
            return
        ws_connection.send(json_data)
        response = ws_connection.recv()
        logger.debug(f'Received from WS server: "{response}"')
        ws_connection.close()
        return response

    def get(self, request, *args, **kwargs):
        return HttpResponse('Not implemented', status=503)

    def post(self, *args, **kwargs):
        raw_body = self.request.body
        try:
            parsed_data = json.loads(raw_body)
            logger.debug(f'Received data : "{parsed_data}"')
        except json.decoder.JSONDecodeError:
            error_msg = 'Invalid JSON Data!'
            logger.error(error_msg)
            return HttpResponse(error_msg, status=400)
        ws_response = self._call_ws_server(raw_body)
        if not ws_response:
            return HttpResponse('Cannot connect to WS server!', status=503)
        return HttpResponse(ws_response, status=200)

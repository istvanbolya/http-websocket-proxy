import logging
import urllib
from socket import error as socket_error
from websockets.sync.client import connect as ws_connect

from django.conf import settings

logger = logging.getLogger(__name__)


def _call_ws_server(json_data):
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

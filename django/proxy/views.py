import json
import logging

from django.http import HttpResponse
from django.views.generic import View

from proxy.tools import _call_ws_server

logger = logging.getLogger(__name__)


class ProxyView(View):

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
        ws_response = _call_ws_server(raw_body)
        if not ws_response:
            return HttpResponse('No response from WS server!', status=503)
        return HttpResponse(ws_response, status=200)

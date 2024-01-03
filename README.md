# http-websocket-proxy
Samples for 'proxy-ing' HTTP POSTs to Websocket calls (POC tests).
The examples under contain a really simple WS server, grabbed from the help of the Websockets documentation.
All of the solutions connects and disconnects on each HTTP POST req.

Error handling:
- invalid URI, HTTP method
- invalid JSON data
- error during WS connection

The different solutions contain redundant code for purpose (i.e WS server, constants): make them work separately, under each own venv. 

Logging is also added to each solution. 

## Django

### Setting up

```    
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run services

- Websocket server: `python3 websocket_server.py`
- Django server: `./manage.py runserver_plus`

### Tests

- Run: `coverage run --source='.' -m pytest`
- Report: `coverage report`


## Flask

### Setting up
    
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run services

- Websocket server: `python3 websocket_server.py`
- Flask server: `python3 flask_server.py`


### Tests

- Run: `coverage run -m pytest`
- Report: `coverage report`


## BaseHTTPServer

### Setting up

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run services

- Websocket server: `python3 websocket_server.py`
- HTTP server: `python3 http_server.py`

### Tests

FYI: the http_server should be started before running the tests: `python3 http_server.py`

- Run: `coverage run -m pytest`
- Report: `coverage report`


## Original task description

```    
# Task description
Implement a simple standalone application which acts as a http (REST) - websocket gateway.
The application "translates" the incoming http requests to websocket requests without changing the incoming JSON content: the same JSON is sent to websocket server that was sent by the http client.
The gateway doesn't change the JSON response of the websocket server - it sends back to the http client without changing it.

# To be implemented
- Simple application
  - listening on localhost:8080
  - exposes an endpoint on POST `/api/ui`
  - forwards the JSON content to websocket server listening on localhost:8081
  - sends back the JSON response to the http client without changing it
- Error handling
- Logging
- Tests
- A README.md file with short description
```    

## Upgrade possibilities:
- Better "cannot be connected" error handling for the WS client. Currently it returns None if error.
- Readable response handling, instead of static numbers (using ie. urllib2.HTTPError.code, http.HTTPStatus)
- Messages to constants, for reusing/translating
- Handle connection error during WS client send
- Handle additional errors from WS server, ie. "Internal error"
- Authentication: basic, token, oauth?
- Flask: make it more "a real app", like in Django. Classes for App, View, URLs, Settings.
- BAseHTTPServer: custom requesthandler mocking, tests
- Support for more URI: 
  - HTTPServer: extend regex, dedicated method for regex route check
  - Flask: additional views/URIs
  - Django: additional views/URLs
- Handle big JSON issue (avoiding possible timeout?)

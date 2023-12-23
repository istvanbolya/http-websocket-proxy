# http-websocket-proxy
Samples for 'proxy-ing' HTTP POSTs to Websocket calls (POC tests).
The examples under contain a really simple WS server, grabbed from the help of the Websockets documentation.
All of the solutions connects and disconnects on each HTTP POST req.

Error handling:
- invalid URI, HTTP method
- invalid JSON data
- error during WS connection

The different solutions contain redundant code for purpose (i.e sw server, constants): make them work separately, under each own venv. 

Logging is also added to each solution. 


## BaseHTTPServer

### Setting up (same in every solution)

```
python3 -m venv venv
source venv/bin/active
pip install -r requirements.txt
```

### Running services

- Websocket server: `python3 websocket_server.py`
- HTTP server: `python3 http_server.py`


## Flask

### Setting up (same in every solution)
    
```
python3 -m venv venv
source venv/bin/active
pip install -r requirements.txt
```

### Running services

- Websocket server: `python3 websocket_server.py`
- Flask server: `python3 flask_server.py`


## Django

### Setting up (same in every solution)

```    
python3 -m venv venv
source venv/bin/active
pip install -r requirements.txt
```

### Running services

- Websocket server: `python3 websocket_server.py`
- Django server: `python3 manage.py runserver_plus`
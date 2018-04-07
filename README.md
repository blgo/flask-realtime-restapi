[![Build Status](https://travis-ci.org/blgo/flask-realtime-restapi.svg?branch=master)](https://travis-ci.org/blgo/flask-realtime-restapi)

## Init virtual environment and Intall Python requirements
```
$ virtualenv .venv

$ . .venv/bin/activate
```

NOTE: On Windows ```$ . .venv/Scripts/activate```

```
$ pip install -r requirements
```

## Run the application
```
$ export FLASK_APP=main.py

$ flask run
```

Alternatively you can use python:

```$ python main.py```

## Externally Visible Server

```$ flask run --host=0.0.0.0```

This tells your operating system to listen on all public IPs.

## Debug mode

Debug mode will use the mock database instead of MongoDB.

```
$ export FLASK_DEBUG=1

$ flask run
```

(On Windows you need to use **set** instead of **export**).

## Docker image

[![](https://images.microbadger.com/badges/image/blgo/flask-realtime-restapi.svg)](https://microbadger.com/images/blgo/flask-realtime-restapi "Get your own image badge on microbadger.com")

[![](https://images.microbadger.com/badges/version/blgo/flask-realtime-restapi.svg)](https://microbadger.com/images/blgo/flask-realtime-restapi "Get your own version badge on microbadger.com")

### Download Docker image

```docker pull blgo/flask-realtime-restapi:latest```

### Run Docker image

Start MongoDB or set FLASK_DEBUG to skip this command:

```docker run --rm -p 27017:27017 -d mongo```

Start Realtimeapp

```docker run --rm -p 80:80 blgo/flask-realtime-restapi:latest```


## TODO
Websockets charts module should not call the database directly. It should usethe API module to retrieve sensor data, readings, etc.
This will require running this module as a separate application, following a Microservices like architecture.

The application should be made out of 3 services:
MongoDB <> REST API > Web UI & Websockets server
(The Web UI is only for monitoring purposes and at the moment does not POST to the REST API)

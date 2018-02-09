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
* Sanitase requirements.txt
* Configure Docker image to run supervisor as a limited access user (currently running on ```root```).
* Use blueprints for restful api and sockets IO in order to be able to create as many "sensor" endpoints as necesary without duplicating code. 
* Add database support.
* Handle Websockets disconnect
* Add basic error handling and logging (docker logs compatible)
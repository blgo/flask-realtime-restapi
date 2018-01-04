## Run the application
`
$ export FLASK_APP=main.py
$ flask run
`

Alternatively you can use python:

`$ python main.py`

## Externally Visible Server

`flask run --host=0.0.0.0`

This tells your operating system to listen on all public IPs.

## Debug mode
`
$ export FLASK_DEBUG=1
$ flask run
`

(On Windows you need to use set instead of export).

## Docker image

### Build Docker image

`docker pull blgo/flask-realtime-restapi:latest`

### Run Docker image

`docker run --rm -p 80:80 blgo/flask-realtime-restapi:latest`


## TODO
* Handle Websockets disconnect
* Add basic error handling and logging (docker logs compatible)
* Use Twitter bootstrap to make the HTML a bit more pretty
* Configure RESTful API to support humidity and temperature sensor data
* Fix favicon error with RESTful API

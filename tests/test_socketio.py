from realtimeapp import configure_app, app
from realtimeapp.socketio import create_socketio, socketio
from flask_socketio import SocketIOTestClient
import time

from nose.tools import *

# Initialise app
app = configure_app()

# Initialise flask-socketio
create_socketio(app)


def connect_client():
    testclient = SocketIOTestClient(app, socketio,"/test",None,None)
    return testclient


def test_ping():
    testclient = connect_client()
    testclient.emit("my_ping", namespace="/test")
    testclient.disconnect("/test")
    items = testclient.get_received(namespace="/test")
    assert_equal(items[0]['args'][0]['data'],"Connected")
    assert_equal(items[1]['name'],"my_pong")


def test_backgroundthreat():
    testclient = connect_client()
    testclient.emit("my_event", {'data': 'Client reponse: I\'m connected!'}, namespace="/test")
    testclient.disconnect("/test")
    items = testclient.get_received(namespace="/test")
    assert_equal(items[0]['args'][0]['data'],"Connected")
    assert_equal(items[1]['args'][0]['data'],"Client reponse: I'm connected!")
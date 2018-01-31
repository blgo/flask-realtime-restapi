from realtimeapp import configure_app, app
from realtimeapp.socketio import create_socketio, socketio
from flask_socketio import SocketIOTestClient
import time
from nose.tools import *

# Initialise app
app = configure_app()

# Initialise flask-socketio
create_socketio(app)


def connect_client(namespace):
    testclient = SocketIOTestClient(app, socketio,namespace,None,None)
    return testclient


def test_ping():
    namespace = "/test"
    testclient = connect_client(namespace)
    testclient.emit("my_ping", namespace=namespace)
    testclient.disconnect("/test")
    items = testclient.get_received(namespace=namespace)
    assert_equal(items[0]['args'][0]['data'],"Connected")
    assert_equal(items[1]['name'],"my_pong")


# def test_backgroundthreat():
#     testclient = connect_client()
#     testclient.emit("my_event", {'data': 'Client reponse: I\'m connected!'}, namespace="/test")
#     testclient.disconnect("/test")
#     items = testclient.get_received(namespace="/test")
#     assert_equal(items[0]['args'][0]['data'],"Connected")
#     assert_equal(items[1]['args'][0]['data'],"Client reponse: I'm connected!")


def test_charts_getdata():
    namespace = "/charts"
    testclient = connect_client(namespace)
    testclient.emit("get-data", namespace=namespace)
    testclient.disconnect(namespace)
    time.sleep(2)
    items = testclient.get_received(namespace=namespace)

    assert_in('2018-01-05 15:49:11.193728',items[1]['args'][0]['label'][0])

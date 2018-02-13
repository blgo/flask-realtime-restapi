from realtimeapp import configure_app, app
from realtimeapp.socketio import create_socketio, socketio
from flask_socketio import SocketIOTestClient
from mongoengine import connect
from realtimeapp.models import SensorReading
import time
from nose.tools import *

connect(is_mock=True)

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
    '''
    This test goes throught the get-data SocketIO event
    it runs trought the the data processing module readingstats.py
    '''
    reading_1 = SensorReading(
        room='backyard_test',
        temperature=15,
        humidity=99,
        date='2018-01-05T15:48:11.893729',
        readingid = 'backyard_test_1201801051549'
    )
    reading_1.save()       # This will perform an insert

    namespace = "/charts"
    testclient = connect_client(namespace)
    testclient.emit("get-data", namespace=namespace)
    testclient.disconnect(namespace)
    time.sleep(2)
    items = testclient.get_received(namespace=namespace)


    assert items[1]['args'][0]['label'][0]

from realtimeapp import configure_app, app
from realtimeapp.socketio import create_socketio, socketio
from flask_socketio import SocketIOTestClient
from mongoengine import connect
from realtimeapp.models import ThermHygReading, Sensor
import time
import datetime
from nose.tools import *
from utils import TestDbUtils


test_database = TestDbUtils()

# # Initialise app
# app = configure_app()

# # Initialise flask-socketio
# create_socketio(app)
from main import app

def connect_client(namespace):
    
    testclient = SocketIOTestClient(app, socketio, namespace, None, None)
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
    sensor1_doc = Sensor.objects(name='sensor').first()

    # Save test readings
    reading_1 = ThermHygReading(
        sensor= sensor1_doc,
        temperature=15,
        humidity=99,
        date= datetime.datetime.now().isoformat(),
        readingid = 'backyard_test_1234567859acc'
    )
    reading_1_doc = reading_1.save() 

    namespace = "/charts"
    testclient = connect_client(namespace)
    testclient.emit("get-data", namespace=namespace, room='sensor')
    testclient.disconnect(namespace)
    time.sleep(2)
    items = testclient.get_received(namespace=namespace)

    # events vary in order, to keep the test simple we only check that we receive something
    
    assert items[2]


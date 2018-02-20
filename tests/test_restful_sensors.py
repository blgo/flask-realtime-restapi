from main import app
from nose.tools import assert_equal, assert_in
from mongoengine import connect
from realtimeapp.restful.resourcessensors import SensorList, SensorResource
from realtimeapp.restful import api
from utils import TestDbUtils 
import json

'''
Requires running a MongoDB instance
docker run --rm -p 270One7:270One7 -d mongo:Three.6.2
''' 

test_database = TestDbUtils()


def test_restfulapi():
    # Initialise Flask in test mode

    app.testing = True

    # Initialise test client
    testapp = app.test_client()

    rv = testapp.post('/sensor', 
        data=dict({"room" : "backyarkTest",
                  "name" : "TestSensorNameOne"})
         ,follow_redirects=True)
    
    data = rv.data.decode("utf-8")

    assert_equal('201 CREATED', rv._status)

    # Check that the sensor is coming back in the response
    assert_in("TestSensorNameOne",data)
    
    testapp.post('/sensor', 
        data=dict({"room" : "backyarkTest",
                  "name" : "TestSensorNameTwo"})
         ,follow_redirects=True)
    

    testapp.post('/sensor', 
        data=dict({"room" : "backyarkTest",
                  "name" : "TestSensorNameThree"})
         ,follow_redirects=True)

    # Check if the list endpoint returns ALL readings and verify that they exist in the results
    
    rv = testapp.get('/sensor', follow_redirects=True) 
    data = rv.data.decode("utf-8")
    
    data_json=json.loads(data)

    assert_equal('TestSensorNameTwo'
    ,data_json.get('sensors')[3]['name'])


    # Test get a specific sensor

    rv = testapp.get('/sensor/TestSensorNameThree',
     follow_redirects=True)
    data = rv.data.decode("utf-8")
    data_json=json.loads(data)

    assert_equal('TestSensorNameThree'
    ,data_json.get('name'))

    # Test Validarte name field

    rv = testapp.post('/sensor', 
        data=dict({"room" : "backyarkTest",
                  "name" : "room3"})
        ,follow_redirects=True)

    # Number 3 is disallowed by inputs validation:
    assert_equal('400 BAD REQUEST', rv._status)


    # Test update existent reading by id
    
    rv = testapp.put('/sensor/TestSensorNameThree', 
        data=dict({"room" : "backyarkTestUpdated",
                  "name" : "TestSensorNameThreeUpdated"})
         ,follow_redirects=True)

    data = rv.data.decode("utf-8")
    data_json=json.loads(data)
    assert_equal('202 ACCEPTED', rv._status)
    
    assert_equal('TestSensorNameThreeUpdated'
    ,data_json.get('name'))
    
    assert_equal('backyarkTestUpdated', data_json.get('room'))

    # Test get the updated sensor

    rv = testapp.get('/sensor/TestSensorNameThree',
     follow_redirects=True)
    data = rv.data.decode("utf-8")
    data_json=json.loads(data)

    # Now, the old sensor name does not exists
    assert not data_json.get('name')

from nose.tools import assert_equal, assert_in
from mongoengine import connect
from realtimeapp.restful.resourcesreadings import ReadingList, Reading
from realtimeapp.restful import api
from utils import TestDbUtils 
from main import app
import json

'''
Requires running a MongoDB instance
docker run --rm -p 27017:27017 -d mongo:3.6.2
''' 

test_database = TestDbUtils()


def test_restfulapi():
    # Initialise Flask in test mode
    app.testing = True



    # Initialise test client
    testapp = app.test_client()
    
    rv = testapp.get('/') 
    data = rv.data.decode("utf-8")

    rv = testapp.post('/reading', 
        data=dict({"date" : "2018-01-05T15:49:11.193728",   
                  "sensor" : "Thermohydrometer",
                  "temperature" : 45,
                  "humidity" : 98})
         ,follow_redirects=True)
    
    
    testapp.post('/reading', 
        data=dict({"date" : "2018-02-05T15:49:11.193728",   
                "sensor" : "Thermohydrometer",
                "temperature" : 45,
                "humidity" : 98})
        ,follow_redirects=True)


    testapp.post('/reading', 
        data=dict({"date" : "2018-02-05T15:59:11.193728",   
                "sensor" : "Thermohydrometer",
                "temperature" : 45,
                "humidity" : 98})
        ,follow_redirects=True)


    data = rv.data.decode("utf-8")

    assert_equal('201 CREATED', rv._status)

    # Check if the room is coming from the sensor registered in the database 
    assert_in("backyard_test",data)

    rv = testapp.get('/reading', follow_redirects=True) 
    data = rv.data.decode("utf-8")

    # Check if the GET endpoint returns ALL the readings and check a few
    data_json=json.loads(data)

    assert_equal('backyard_test_1234567859abc'
    ,data_json.get('readings')[0]['readingid'])


    rv = testapp.post('/reading', 
        data=dict({"date" : "2018-01-0515:49:11.193728",   
                  "sensor" : "Thermohydrometer",
                  "temperature" : 45,
                  "humidity" : 98})
    )

    assert_equal('400 BAD REQUEST', rv._status)

    # Add more data
    rv = testapp.post('/reading', 
        data=dict({"date" : "2018-01-06T15:49:11.193728",   
                  "sensor" : "Thermohydrometer",
                  "temperature" : 45,
                  "humidity" : 98})
         ,follow_redirects=True)


    # Test add reading from unregistered sensor
    rv = testapp.post('/reading', 
        data=dict({"date" : "2018-02-05T15:49:11.193728",   
                "sensor" : "Unregistered",
                "temperature" : 45,
                "humidity" : 98})
        ,follow_redirects=True)

    data = rv.data.decode("utf-8")

    assert_equal('404 NOT FOUND', rv._status)

    # Test get existent reading

    rv = testapp.get('/reading/backyard_test_1234567859abc',
     follow_redirects=True)
    data = rv.data.decode("utf-8")
    data_json=json.loads(data)

    assert_equal('backyard_test_1234567859abc'
    ,data_json.get('readingid'))  

    # Test get non existent reading by id

    rv = testapp.get('/reading/this_id_doesnt_exists',
     follow_redirects=True)

    assert_equal('404 NOT FOUND', rv._status)
    

    # Test update existent reading by id
    
    rv = testapp.put('/reading/backyard_test_1234567859abc', 
        data=dict({
            "sensor": "Thermohydrometer",
            "date": "2018-02-19T17:26:01.354902",
            "temperature" : 0,
            "humidity" : 1})
        ,follow_redirects=True)

    data = rv.data.decode("utf-8")
    data_json=json.loads(data)
    assert_equal('202 ACCEPTED', rv._status)
    
    assert_equal('backyard_test_1234567859abc'
    ,data_json.get('readingid'))
    
    assert_equal(0, data_json.get('temperature'))

    assert_equal(1, data_json.get('humidity'))

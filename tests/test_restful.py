from realtimeapp import *
from realtimeapp.restful import create_api
from nose.tools import *
from flask import request

def test_addreading():
    app = configure_app()
    app.testing = True
    create_api(app)
    testapp = app.test_client()
    rv = testapp.get('/') 
    data = rv.data.decode("utf-8")

    rv = testapp.post('/sensor1', 
        data=dict({"date" : "2018-01-05T15:49:11.193728+00:00",   
                  "room" : "test_backyard",
                  "temperature" : 45,
                  "humidity" : 98})
         ,follow_redirects=True)
     
    data = rv.data.decode("utf-8")
    assert_equal('201 CREATED', rv._status)
    assert_in("test_backyard",data)

    rv = testapp.get('/sensor1', follow_redirects=True) 
    data = rv.data.decode("utf-8")

    assert_in('test_backyard',data)

    rv = testapp.post('/sensor1', 
        data=dict({"date" : "2018-01-0515:49:11.193728+00:00",   
                  "room" : "test_backyard",
                  "temperature" : 45,
                  "humidity" : 98})
    )
     
    assert_equal('400 BAD REQUEST', rv._status)

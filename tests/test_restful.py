from realtimeapp import configure_app
from nose.tools import assert_equal, assert_in
from realtimeapp.restful.resources import ReadingList
from realtimeapp.restful import api

'''
Requires running a MongoDB instance
docker run --rm -p 27017:27017 -d mongo:3.6.2
''' 

def test_addreading():
    # Initialise Flask in test mode
    app = configure_app()
    app.testing = True

    # Initialise Flask-RESTful api
    api.add_resource(ReadingList, '/sensor1')
    api.init_app(app)

    # Initialise test client
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
    
    # Add more data
    rv = testapp.post('/sensor1', 
        data=dict({"date" : "2018-01-06T15:49:11.193728+00:00",   
                  "room" : "test_backyard",
                  "temperature" : 45,
                  "humidity" : 98})
         ,follow_redirects=True)
    
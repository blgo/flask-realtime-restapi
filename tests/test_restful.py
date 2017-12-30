from realtimeapp import *
from realtimeapp.restful import create_api
from nose.tools import *
from flask import request

def test_addtodo():
    app = configure_app()
    app.testing = True
    create_api(app)
    testapp = app.test_client()
    rv = testapp.get('/') 
    data = rv.data.decode("utf-8")

    rv = testapp.put('/todo1', data=dict(
        data="works"
    ), follow_redirects=True)
     
    data = rv.data.decode("utf-8")

    assert_in(data,'{"todo1": "works"}\n')

    rv = testapp.get('/todo1') 
    data = rv.data.decode("utf-8")

    assert_equal(data,'{"todo1": "works"}\n')

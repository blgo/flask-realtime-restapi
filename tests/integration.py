import requests
from time import sleep
import json
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
'''
This test is design to run using a running Docker image, configured for
 Travis CI. 
'''

# Setup Requests
url = 'http://localhost/sensor1'
data = { "date" : "2018-01-06T15:48:11.893728+00:00",
        "room" : "bedroom", 
        "temperature" : 10, 
        "humidity" : 10 } 
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# POST to RESTapi
post = requests.post(url, data=json.dumps(data), headers=headers)
print (post)
assert post.ok

# GET from RESTapi
get = requests.get(url + '/bedroom20184806150111893728')
print(get)
assert get.ok


# Socket.IO setup

class ChartNamespace(BaseNamespace):

    def my_response(self, *args):
        print('my_response', args)
        assert 'Chart data stream Connected' == args[0]['data']

    def my_chart(self, *args):
        print('my_chart', args)
        assert 10.0 == args[0]['dataa']


    def my_chart_stats(self, *args):
        print('my_chart_stats', args)
        assert 10.0 == args[0]['tempmean']


# Socket.IO tests
socketIO = SocketIO('localhost', 80, wait_for_connection=False)
chart_namespace = socketIO.define(ChartNamespace, '/charts')

chart_namespace.emit('get-data')

chart_namespace.on('my_response', chart_namespace.my_response)
chart_namespace.on('my_chart', chart_namespace.my_chart)
chart_namespace.on('my_chart_stats', chart_namespace.my_chart_stats)

socketIO.wait(seconds=2)

import requests
from time import sleep
import json
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace
import datetime
'''
This test is design to run using a running Docker image, configured for
 Travis CI. 
'''

# Setup Requests
url = 'http://localhost/reading'
date = datetime.datetime.now()
datestr = date.isoformat()
data = { "date" : datestr,
        "sensor" : "sensor", 
        "temperature" : 10, 
        "humidity" : 10 } 
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# POST to RESTapi
post = requests.post(url, data=json.dumps(data), headers=headers)
print (post)
assert post.ok

# GET from RESTapi
datestr=date.strftime("%Y%M%d%H%m%S%f")
reading_id = "{0}{1}".format("room", datestr )
get = requests.get(url + '/' + reading_id)
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

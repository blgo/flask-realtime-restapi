import requests
from time import sleep
import json

'''
This test is design to run using a running Docker image, configured for
 Travis CI. 
'''

sleep(5)
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
if not post.ok:
    exit(1)

# GET from RESTapi
get = requests.get(url + '/bedroom20184806150111893728')
print(get)
if not get.ok:
    exit(1)

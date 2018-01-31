import requests
import datetime
from time import sleep
from random import randint
import json
'''
Send a request every second to the RESTful API.
It should display in an open webbrowser on http://localhost:5000
'''
while True:
    sleep(1)
    url = 'http://localhost:5000/sensor1'
    data = { "date" : datetime.datetime.now().isoformat(), "room" : "bedroom", "temperature" : str(randint(10, 20)), "humidity" : str(randint(45, 65)) } 
    print(json.dumps(data))
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    requests.post(url, data=json.dumps(data), headers=headers)

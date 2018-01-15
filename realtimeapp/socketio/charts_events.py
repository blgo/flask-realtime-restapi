from flask import session
from flask_socketio import emit
from threading import Lock
from . import socketio
from ..serializers import THERMOHYGRO
from ..serializers.convertochartsjs import generate_stats_from_raw

from random import randint
import datetime
import json


chart_thread = None
chart_thread_lock = Lock()

@socketio.on('connect', namespace='/charts')
def charts_connect():
    print("Server says: A client has connected to charts")
    emit('my_response', {'data': 'Connected', 'count': 0})


def chart_background_thread():
    reading_ids=[]
    while True:
        readings_list = dict.items(THERMOHYGRO)
        for readings_touples in readings_list:
            
            if readings_touples[0] not in reading_ids:
                
                reading_ids.append(readings_touples[0])
                temperature=readings_touples[1]['temperature']
                humidity=readings_touples[1]['humidity']
                date=readings_touples[1]['date']
                socketio.emit('my_chart', {'label': date, 'dataa': temperature, 'datab': humidity }, namespace='/charts')

                json_stats = generate_stats_from_raw(THERMOHYGRO)
                socketio.emit('my_chart_stats', json_stats, namespace='/charts')


        socketio.sleep(1)


@socketio.on('get-data', namespace='/charts')
def get_chart_data():
    print("Server says: Chart data requested from the client")
    global chart_thread
    with chart_thread_lock:
        if chart_thread is None:
            chart_thread = socketio.start_background_task(target=chart_background_thread)
    emit('my_response', {'data': 'Chart data stream Connected', 'count': 0}, namespace="/charts")

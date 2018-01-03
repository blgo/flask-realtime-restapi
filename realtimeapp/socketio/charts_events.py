from flask import session
from flask_socketio import emit
from threading import Lock
from . import socketio

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
    while True:
        socketio.sleep(5)
        chart_data = get_graph_data()
        socketio.emit('my_chart', {'label': chart_data[0], 'dataa': chart_data[1], 'datab': chart_data[2] }, namespace='/charts')



@socketio.on('get-data', namespace='/charts')
def get_chart_data():
    print("chart data requested from the client")
    global chart_thread
    with chart_thread_lock:
        if chart_thread is None:
            chart_thread = socketio.start_background_task(target=chart_background_thread)
    emit('my_response', {'data': 'Chart data stream Connected', 'count': 0}, namespace="/charts")

def get_graph_data():
    # graph_to_send = json.dumps({
    #     'x': ctime(),
    #     'y':'100'
    # })
    return datetime.datetime.now().isoformat(), randint(0, 50), randint(0, 100)
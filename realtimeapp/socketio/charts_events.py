from flask_socketio import emit
from threading import Lock
from . import socketio
from ..readingstats import readings_to_matrix, generate_stats, transpose_readings
from ..models import return_all_by_date, last_reading


from random import randint
import datetime
import json


# chart_thread = None
# chart_thread_lock = Lock()

@socketio.on('connect', namespace='/charts')
def charts_connect():
    print("Server says: A client has connected to charts")
    emit('my_response', {'data': 'Connected', 'count': 0})


# def chart_background_thread():
#     while True:
#          for readings_touples in readings_matrix:
#          socketio.sleep(1)

@socketio.on('get-data', namespace='/charts')
def get_chart_data():
    print("Server says: Chart data requested from the client")

    # global chart_thread
    # with chart_thread_lock:
    #     if chart_thread is None:
    #         chart_thread = socketio.start_background_task(target=chart_background_thread)



    THERMOHYGRO = return_all_by_date(days=1)
    if THERMOHYGRO:
        readings_matrix = readings_to_matrix(THERMOHYGRO)
        transposed_readings = transpose_readings(readings_matrix)
        last=last_reading()
        emit('last_reading', {'label': str(last['date']), 'dataa':  last['temperature'], 'datab':  last['humidity'] }, last='/charts')
        emit('my_chart_init', {'label': transposed_readings[1].tolist(),
             'dataa':  transposed_readings[2].tolist(),
             'datab':  transposed_readings[3].tolist() },
             namespace='/charts')
        stats = generate_stats(THERMOHYGRO)
        emit('my_chart_stats', stats, namespace='/charts')

    else:
        emit('last_reading', {'label': [] , 'dataa': [] , 'datab': [] }, namespace='/charts')
        emit('my_chart_init', {'label': [] , 'dataa': [] , 'datab': [] }, namespace='/charts')
        emit('my_chart_stats', {}, namespace='/charts')

    emit('my_response', {'data': 'Chart data stream Connected', 'count': 0}, namespace="/charts")

def emit_new_reading(reading):
    
    THERMOHYGRO = return_all_by_date(days=1)
    if THERMOHYGRO:
        socketio.emit('last_reading', {'label': reading['date'] , 'dataa':  reading['temperature'], 'datab':  reading['humidity'] }, namespace='/charts')
        socketio.emit('my_chart', {'label': reading['date'] , 'dataa':  reading['temperature'], 'datab':  reading['humidity'] }, namespace='/charts')
        stats = generate_stats(THERMOHYGRO)
        socketio.emit('my_chart_stats', stats, namespace='/charts')
    
    socketio.emit('my_response', {'data': 'Data received from sensor', 'count': 0}, namespace="/charts")

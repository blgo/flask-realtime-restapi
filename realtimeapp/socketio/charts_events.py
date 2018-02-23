from flask_socketio import emit, join_room, leave_room
from threading import Lock
from . import socketio
from ..readingstats import readings_to_matrix, generate_stats, transpose_readings
from ..models import return_all_by_date, last_reading
from flask import session

from random import randint
import datetime
import json


# chart_thread = None
# chart_thread_lock = Lock()

@socketio.on('connect', namespace='/charts')
def charts_connect():
    print(session['sensor_name'],"Server says: A client has connected to charts")
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('get-data', namespace='/charts')
def get_chart_data():
    print("Server says: Chart data requested from the client")
    session['session_active']=True
    print(session.get('sensor_name'), ' - get-data')
    # global chart_thread
    # with chart_thread_lock:
    room = session.get('sensor_name')
    join_room(room)
    emit('my_response', {'data': 'Started new ' + session.get('sensor_name') + ' thread to keep client chart up-to-date', 'count': 0}, room=room)
    # if chart_thread is None:
    chart_thread = socketio.start_background_task(target=emit_new_reading, session=session._get_current_object())

    THERMOHYGRO = return_all_by_date(days=1, name=session.get('sensor_name'))
    # Pre-populate chart with existent data
    if THERMOHYGRO:
        readings_matrix = readings_to_matrix(THERMOHYGRO)
        transposed_readings = transpose_readings(readings_matrix)
        last=last_reading()
        emit('last_reading', {'label': str(last['date'].isoformat()), 'dataa':  last['temperature'], 'datab':  last['humidity'] },  room=room)
        emit('my_chart_init', {'label': transposed_readings[1].tolist(),
             'dataa':  transposed_readings[2].tolist(),
             'datab':  transposed_readings[3].tolist() },
              room=room)
        stats = generate_stats(THERMOHYGRO)
        emit('my_chart_stats', stats, room=room)
    # Create placeholder blanck chart when database is empty 
    else:
        emit('last_reading', {'label': [] , 'dataa': [] , 'datab': [] }, room=room)
        emit('my_chart_init', {'label': [] , 'dataa': [] , 'datab': [] }, room=room)
        emit('my_chart_stats', {}, room=room)

    emit('my_response', {'data': 'Chart data stream Connected', 'count': 0}, room=room)


def emit_new_reading(session):
    print(session.get('sensor_name'), ' - thread off loop')
    print(session.get('session_active'), ' - thread off loop')



    while session.get('session_active'):
        room = session.get('sensor_name')
        THERMOHYGRO = return_all_by_date(days=1, name=session.get('sensor_name'))
        socketio.sleep(2)
        if  THERMOHYGRO:
            print(session.get('sensor_name'), ' - thread in loop')
            print(session.get('session_active'), ' - thread in loop')
            last=last_reading()
            socketio.emit('last_reading', {'label': str(last['date'].isoformat()) , 'dataa':  last['temperature'], 'datab':  last['humidity'] }, namespace="/charts", room=room)
            socketio.emit('my_chart', {'label': str(last['date'].isoformat()) , 'dataa':  last['temperature'], 'datab':  last['humidity'] }, namespace="/charts", room=room)
            stats = generate_stats(THERMOHYGRO)
            socketio.emit('my_chart_stats', stats, namespace="/charts", room=room)
            socketio.emit('my_response', {'data': 'Data received from sensor', 'count': 0}, namespace="/charts", room=room)


@socketio.on('disconnect', namespace='/charts')
def charts_disconnect():
    room = session.get('sensor_name')
    print(session.get('sensor_name'), ' - diconnect ')
    session['session_active']=False
    emit('my_response', {'data': 'Connected', 'count': 0}, room=room)
    leave_room(room)

from flask_socketio import emit, join_room, leave_room
from threading import Lock
from . import socketio
from ..readingstats import readings_to_matrix, generate_stats, transpose_readings
from ..models import return_all_by_date, last_reading, get_sensor_name_from_readingid
from flask import session

from random import randint
import datetime
import json


@socketio.on('connect', namespace='/charts')
def charts_connect():
    print(session.get('sensor_name','sesion'),"Server says: A client has connected to charts")
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('get-data', namespace='/charts')
def get_chart_data():
    print("Server says: Chart data requested from the client")
    session['session_active']=True
    print(session.get('sensor_name','sensor'), ' - get-data')

    room = session.get('sensor_name','sensor')
    join_room(room)
    emit('my_response', {'data': 'Chart data stream Connected', 'count': 0}, room=room)


    THERMOHYGRO = return_all_by_date(days=1, name=session.get('sensor_name','sensor'))
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


def emit_new_reading(reading):
    # This method is a singleton which does not access request or app context
    # I want to emit the new readings to the client webbrowsers connected to speific socketIO room for the sensor
    # Get the sensor name from the received data in the REST api
    sensor_name = get_sensor_name_from_readingid(reading['readingid'])

    THERMOHYGRO = return_all_by_date(days=1, name=sensor_name)
    if  THERMOHYGRO:

        socketio.emit('last_reading', {'label': reading['date'] , 'dataa':  reading['temperature'], 'datab':  reading['humidity'] }, namespace="/charts", room=sensor_name)
        socketio.emit('my_chart', {'label': reading['date'] , 'dataa':  reading['temperature'], 'datab':  reading['humidity'] }, namespace="/charts", room=sensor_name)
        
        # I should use a server background event to update stats everyminute.
        stats = generate_stats(THERMOHYGRO)
        socketio.emit('my_chart_stats', stats, namespace="/charts", room=sensor_name)
        socketio.emit('my_response', {'data': 'Data received from sensor', 'count': 0}, namespace="/charts", room=sensor_name)


@socketio.on('disconnect', namespace='/charts')
def charts_disconnect():
    room = session.get('sensor_name','sensor')
    print(session.get('sensor_name','sensor'), ' - disconnect')
    session['session_active']=False
    emit('my_response', {'data': 'Connected', 'count': 0}, room=room)
    leave_room(room)


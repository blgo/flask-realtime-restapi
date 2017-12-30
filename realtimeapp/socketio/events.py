from flask_socketio import emit
from . import socketio

@socketio.on('connect')
def test_message():
    print("Server says: A client has connected")

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


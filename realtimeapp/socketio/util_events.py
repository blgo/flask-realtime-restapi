from flask import session
from flask_socketio import emit
# from threading import Lock
from . import socketio

# thread = None
# thread_lock = Lock()

# def test_background_thread():
#     """Example of how to send server generated events to clients."""
#     count = 0
#     while True:
#         socketio.sleep(10)
#         count += 1
#         socketio.emit('my_response',
#                       {'data': 'Server generated event', 'count': count},
#                         namespace='/test')


@socketio.on('connect', namespace='/test')
def test_connect():
    print("Server says: A client has connected")
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(target=test_background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

from flask import Flask, render_template, request
from flask_restful import Api
from flask_socketio import SocketIO, emit
from threading import Lock
import eventlet

from realtimeapp.resources.restfulapi import TodoSimple


app = Flask(__name__)
app.config['SECRET_KEY'] = "verysecret"


# RESTful api
# Add data to the server using: curl http://localhost:5000/todo1 -d "data=it works!" -X PUT
api = Api(app)
api.add_resource(TodoSimple, '/<string:todo_id>')


# Websockets eventlet
async_mode = 'eventlet'
socketio = SocketIO(app, async_mode=async_mode)


thread = None
thread_lock = Lock()

        # # use websockets in background when new data is created
        # global thread
        # with thread_lock:
        #     thread = socketio.start_background_task(target=background_thread)


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0

    if todos.get("todo1"):
        socketio.emit('my_restful_data',
                    {'data': todos["todo1"], 'count': count},
                    namespace='/test')


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_message():
    print("Server says: A client has connected")

@socketio.on('connect', namespace='/test')
def test_connect():
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


if __name__ == '__main__':
    socketio.run(app, debug=True)
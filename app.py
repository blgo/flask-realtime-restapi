from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet

async_mode = 'eventlet'
app = Flask(__name__)
app.config['SECRET_KEY'] = "verysecret"
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('my_event')
def test_message(message):
    emit('my_response', {'data': message['data']})

@socketio.on('disconnect')
def test_message():
    print("Server says: A client has disconnected")

@socketio.on('connect')
def test_message():
    print("Server says: A client has connected")

@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')



if __name__ == '__main__':
    socketio.run(app, debug=True)

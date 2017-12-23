from flask import Flask
from flask_socketio import SocketIO
import eventlet

# Websockets eventlet
async_mode = 'eventlet'
socketio = SocketIO()

def create_app(debug=False):
    """Create an application."""

    app = Flask(__name__)
    app.config['SECRET_KEY'] = "verysecret"
    
    from . import events

    socketio.init_app(app, async_mode=async_mode)
    return app
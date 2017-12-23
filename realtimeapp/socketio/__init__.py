from flask_socketio import SocketIO
import eventlet

async_mode='eventlet'
socketio = SocketIO()

def create_socketio(app):
    """Create an application."""

    from . import events

    socketio.init_app(app, async_mode=async_mode)
    return app
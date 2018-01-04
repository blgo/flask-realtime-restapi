from realtimeapp import configure_app, app
from realtimeapp.socketio import create_socketio, socketio
from realtimeapp.restful import create_api

# Initialise app
app = configure_app()

# Initialise restful api
create_api(app)

# Initialise flask-socketio
create_socketio(app)

if __name__ == '__main__':
    # the start point is socketio.run() uses eventlet which provides a production ready 
    socketio.run(app)

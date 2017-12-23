from realtimeapp import configure_app, app
from realtimeapp.socketio import create_socketio, socketio
from realtimeapp.restful import create_api#, api

# Initialise app
app = configure_app(debug=True)

# Initialise restful api
# Test endpoint: # curl http://localhost:5000/todo1 -d "data=it works!" -X PUT
create_api(app)

# Initialise flask-socketio
create_socketio(app)

if __name__ == '__main__':
    socketio.run(app)
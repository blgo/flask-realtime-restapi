
# from threading import Lock
from flask import render_template

from realtimeapp import configure_app, app
from realtimeapp.socketio import create_socketio, socketio
from realtimeapp.restful import create_api#, api

# Initialise app
app = configure_app(debug=True)

# Test endpoint: # curl http://localhost:5000/todo1 -d "data=it works!" -X PUT
create_api(app)
create_socketio(app)



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
from realtimeapp import configure_app, app, create_api
from realtimeapp.socketio import create_socketio, socketio
from mongoengine import connect
from os import environ

# Initialise app
app = configure_app()

# Initialise restful api
create_api(app)

# Initialise flask-socketio
create_socketio(app)

if __name__ == '__main__':
    # the start point is socketio.run() uses eventlet which provides a production ready 
    # Establishing a Connection
    if not environ.get('FLASK_DEBUG', None): 
        connect('mongoengine', host='localhost', port=27017)
        print('Connected to MongoDB instance in localhost')
        print('If you are testing and need a mock database use: $ export FLASK_DEBUG=1')
    else:
        connect('mongoengine_test', is_mock=True)
        print('Connected to mock database.')
        

    socketio.run(app)

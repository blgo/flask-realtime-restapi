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

if not environ.get('FLASK_DEBUG', None): 
    mongodb_location = environ.get('MONGODB_NETWORK_ALIAS', "localhost")
    connect('mongoengine', host=mongodb_location, port=27017)
    print('Connected to MongoDB instance in ', mongodb_location)
    print('If you are testing and need a mock database use: $ export FLASK_DEBUG=1')
else:
    connect('mongoengine_test', is_mock=True)
    print('Connected to mock database.')

# Add default sensor if it does not exists in MongoDB
from realtimeapp.models import Sensor
sensor = Sensor.objects(name='sensor')
if not sensor:
    sensor = Sensor(room='room', name='sensor')
    sensor.save()


if __name__ == '__main__':
    # the start point is socketio.run() uses eventlet which provides a production ready 
    # Establishing a Connection

    socketio.run(app)

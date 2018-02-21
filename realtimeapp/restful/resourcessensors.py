from flask_restful import Resource, reqparse, abort, inputs
from flask_restful import Resource, fields, marshal_with

from . import api

from ..models import Sensor

# Serialise response using fields and marshall_with 

sensor_fields = {
    'name' : fields.String,
    'room' : fields.String
}

sensorlist_fields = {
    'sensors': fields.List(fields.Nested(sensor_fields))
}

# REST API input data is parsed using reqparser
parser = reqparse.RequestParser()
parser.add_argument('room',type=inputs.regex('^\D+$'), 
    help="<room> has to be a word 'string' without spaces")
parser.add_argument('name',type=inputs.regex('^\D+$'), 
     help="<name> has to be a word 'string' without spaces")

# curl http://localhost:5000/reading1 -H "Content-Type: application/json" -d '{ "date" : "2018-01-05T15:48:11.893728",  "room" : "bedroom", "temperature" : 25, "humidity" : 51 }' -X POST 
# Python can generate this date: 
# datetime.datetime.now().isoformat()

def find_sensor_by_name(name):
    '''
    Return database sensor by name
    '''
    for sensor in Sensor.objects(name=name):
        return sensor

def abort_if_data_doesnt_exist(name):
    sensor = find_sensor_by_name(name)
    if not sensor:
        abort(404, message="Sensor {} doesn't exist".format(name))
    return sensor

class SensorResource(Resource):
    @marshal_with(sensor_fields)
    def get(self, name):
        return abort_if_data_doesnt_exist(name), 200

    @marshal_with(sensor_fields)
    def delete(self, name):
        sensor = abort_if_data_doesnt_exist(name)
        sensor.delete

        return "{'message' : 'Sensor and SensorReadings referencing it have been deleted' }", 204

    # Intended to update temperature and humidity only, date and room are readonly
    @marshal_with(sensor_fields)
    def put(self, name):
        args = parser.parse_args()
        sensor = abort_if_data_doesnt_exist(name)

        sensor.room = args['room']
        sensor.name = args['name']
        
        sensor.save()

        return sensor, 202


class SensorList(Resource):
    @marshal_with(sensorlist_fields)
    def get(self, **kwargs):
        sensors = list(Sensor.objects)
        return {'sensors' : list(sensors)}, 200

    @marshal_with(sensor_fields)
    def post(self, **kwargs):
        args = parser.parse_args()

        sensor = Sensor( 
                        room = args['room'],
                        name = args['name']
        )
        sensor.save()

        return sensor, 201

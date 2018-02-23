from flask_restful import Resource, reqparse, abort, inputs
from flask_restful import Resource, fields, marshal_with

from . import api

from ..models import ThermHygReading, SensorReading, Sensor

# Serialise response using fields and marshall_with 


resource_fields = {
    'readingid' : fields.String,
    'room' : fields.String(attribute='sensor.room'),
    'temperature': fields.Float,
    'humidity': fields.Float,
    'date': fields.DateTime(dt_format='iso8601'),
}

resourcelist_fields = {
    'readings': fields.List(fields.Nested(resource_fields))
}

# REST API input data is parsed using reqparser
parser = reqparse.RequestParser()
parser.add_argument('date',type=inputs.datetime_from_iso8601 , 
    help="<date> has to be in datetime isoformat: 2018-01-05T15:48:11.893728 `datetime.datetime.now().isoformat()`")
parser.add_argument('sensor',type=inputs.regex('^\D+$'), 
     help="<sensor> has to be a word 'string' and has to be registered in the database")
parser.add_argument('temperature',type=float , 
    help="<temperature> has to be a number 'float'")
parser.add_argument('humidity',type=float , 
    help="<temperature> has to be a number 'float'")


# curl http://localhost:5000/reading1 -H "Content-Type: application/json" -d '{ "date" : "2018-01-05T15:48:11.893728",  "sensor" : "sensor", "temperature" : 25, "humidity" : 51 }' -X POST 
# Python can generate this date: 
# datetime.datetime.now().isoformat()

def find_reading_by_id(reading_id):
    '''
    Return database reading by id
    '''
    for reading in ThermHygReading.objects(readingid=reading_id):
        return reading


def abort_if_data_doesnt_exist(reading_id):
    reading = find_reading_by_id(reading_id)
    if not reading:
        abort(404, message="Sensor reading {} doesn't exist".format(reading_id))
    return reading

def get_sensor_abort_if_doesnt_exist(sensor_name):
    try:
        sensor = Sensor.objects(name=sensor_name)[0]
    except:
        abort(404, message="Sensor {} not registered in the database".format(sensor_name))
    return sensor

class Reading(Resource):
    @marshal_with(resource_fields)
    def get(self, reading_id):
        reading = abort_if_data_doesnt_exist(reading_id)
        
        return reading, 200

    @marshal_with(resource_fields)
    def delete(self, reading_id):
        reading = abort_if_data_doesnt_exist(reading_id)
        reading.delete

        return "{'message' : 'Data was deleted' }", 204

    # Intended to update temperature and humidity only, date and room are readonly
    @marshal_with(resource_fields)
    def put(self, reading_id):
        args = parser.parse_args()
        reading = abort_if_data_doesnt_exist(reading_id)

        reading.temperature = float('{:.3}'.format(args['temperature']))
        reading.humidity = float('{:.3}'.format(args['humidity']))
        
        reading.save()

        return reading, 202


class ReadingList(Resource):
    @marshal_with(resourcelist_fields)
    def get(self, **kwargs):
        readings = list(SensorReading.objects)
        return {'readings' : list(readings)}, 200

    @marshal_with(resource_fields)
    def post(self, **kwargs):
        args = parser.parse_args()
        sensor_name = args['sensor']
        sensor_doc = get_sensor_abort_if_doesnt_exist(sensor_name)
        date = args['date']
        reading_id = "{0}{1}".format(sensor_doc.room, date.strftime("%Y%M%d%H%m%S%f"))

        reading = ThermHygReading( 
                        readingid = reading_id,
                        date = date.replace(microsecond=0),
                        sensor = sensor_doc,
                        temperature = float('{0:.2f}'.format(args['temperature'])),
                        humidity = float('{0:.2f}'.format(args['humidity']))
        )
        reading.save()

        return reading, 201

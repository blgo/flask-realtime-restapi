from flask import request
from flask_restful import Resource, reqparse, abort, inputs
import datetime
from . import api
from ..serializers import THERMOHYGRO

# TODO: Use https://flask-restful.readthedocs.io/en/latest/quickstart.html#data-formatting
# Sensor dictionary for temperature/humidity reading
# THERMOHYGRO = {
#     <string:RoomNameYYYYMMDDHHmmss> : { 'date': <datetime.isoformat>,
#                                         'room' = <string: room name>,
#                                         'temperature': <int:Celcius>,
#                                         'humidity': <int> },
#     (...)
# }


parser = reqparse.RequestParser()
parser.add_argument('date',type=inputs.datetime_from_iso8601 , 
    help="<date> has to be in datetime isoformat: 2018-01-05T15:48:11.893728 `datetime.datetime.now().isoformat()`")
parser.add_argument('room',type=inputs.regex('^\D+$')  , 
    help="<room> has to be a word 'string'")
parser.add_argument('temperature',type=int , 
    help="<temperature> has to be a number 'int'")
parser.add_argument('humidity',type=int , 
    help="<temperature> has to be a number 'int'")


# curl http://localhost:5000/thermohygro -H "Content-Type: application/json" -d '{ "date" : "2018-01-05T15:48:11.893728+00:00",  "room" : "bedroom", "temperature" : 25, "humidity" : 51 }' -X POST 
# Python can generate this date: 
# datetime.datetime.now().isoformat()

def abort_if_data_doesnt_exist(reading_id):
    if reading_id not in THERMOHYGRO:
        abort(404, message="Sensor reading {} doesn't exist".format(reading_id))


class Reading(Resource):
    def get(self, reading_id):
        abort_if_data_doesnt_exist(reading_id)
        return THERMOHYGRO[reading_id]

    def delete(self, reading_id):
        abort_if_data_doesnt_exist(reading_id)
        del THERMOHYGRO[reading_id]
        return '', 204

    def put(self, reading_id):
        args = parser.parse_args()
        readingdata = { 'date': str(args['date']),
                        'room': args['room'],
                        'temperature': args['temperature'],
                        'humidity': args['humidity'],
        }
        THERMOHYGRO[reading_id] = readingdata
        return readingdata, 201


class ReadingList(Resource):
    def get(self):
        return THERMOHYGRO

    def post(self):
        print(THERMOHYGRO)
        args = parser.parse_args()
        room =  args['room']
        date = args['date']
        print(date)
        print(str(date))
        reading_id = "{0}{1}".format(room, date.strftime("%Y%M%d%H%m%S%f"))
        readingdata = {  'date': str(date),
                        'room': room,
                        'temperature': args['temperature'],
                        'humidity': args['humidity']
        }
        THERMOHYGRO[reading_id] = readingdata
        return THERMOHYGRO[reading_id], 201


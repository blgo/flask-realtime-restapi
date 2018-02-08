from mongoengine import *

# TODO: Use https://flask-restful.readthedocs.io/en/latest/quickstart.html#data-formatting
# Sensor dictionary for temperature/humidity reading
# THERMOHYGRO = {
#     <string:RoomNameYYYYMMDDHHmmss> : { 'date': <datetime.isoformat>,
#                                         'room': <string: room name>,
#                                         'temperature': <int:Celcius>,
#                                         'humidity': <int> },
#     (...)
# }

# Establishing a Connection
connect('mongoengine', host='localhost', port=27017)


# Defining a Document
class SensorReading(Document):
    date =  DateTimeField()
    room = StringField(required=True)
    temperature = FloatField(required=True)
    humidity =  FloatField(required=True)

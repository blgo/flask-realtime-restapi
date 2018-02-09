from mongoengine import connect, Document, StringField, FloatField
import datetime

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
    #TODO: Create resource_fields for returning a list of dictionaries from a list of reading objects 
    #Then, we could save date as a datetime object
    date =  StringField(required=True)
    room = StringField(required=True)
    temperature = FloatField(required=True)
    humidity =  FloatField(required=True)
    readingid = StringField(primary_key=True, required=True)

def return_all():
    readings = {}
    for reading in SensorReading.objects:
        #TODO: Create resource_fields for returning a list of dictionaries from a list of reading objects 
        data = reading._data
        reading_id = data.pop('readingid')
        readings[reading_id]=data
    
    return readings

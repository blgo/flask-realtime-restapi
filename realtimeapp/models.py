from mongoengine import connect, Document, StringField, FloatField, DateTimeField, ReferenceField
from datetime import datetime, timedelta

# Sensor dictionary for temperature/humidity reading
# THERMOHYGRO = {
#     <string:RoomNameYYYYMMDDHHmmss> : { 'date': <datetime.isoformat>,
#                                         'room': <string: room name>,
#                                         'temperature': <int:Celcius>,
#                                         'humidity': <int> },
#     (...)
# }

# class Room(Document):
#     '''
#     Register room
#     '''
#     name = StringField(max_length=50, required=True)

class Sensor(Document):
    '''
    Register sensor
    '''
    name = StringField(max_length=50, required=True)
    room = StringField(max_length=50, required=True)
    

class SensorReading(Document):
    sensor = ReferenceField(Sensor)
    date =  DateTimeField(required=True)
    readingid = StringField(max_length=50, primary_key=True, required=True)

    meta = {'allow_inheritance': True}


# This class will be moved into the sensor specific Blueprint 
class ThermHygReading(SensorReading):
    #TODO: Create resource_fields for returning a list of dictionaries from a list of reading objects 
    #Then, we could save date as a datetime object
    temperature = FloatField(required=True)
    humidity =  FloatField(required=True)


# The following methods query the entire database for Readings. These will need refactoring, and located in the sensor specific Bluewprints.

def return_all():
    readings = {}
    for reading in SensorReading.objects:
        #TODO: Create resource_fields for returning a list of dictionaries from a list of reading objects 
        data = reading._data
        reading_id = data.pop('readingid')
        data['date']=str(data.pop('date').isoformat())
        readings[reading_id]=data
    
    return readings

def return_all_by_date(days):
    readings = {}
    datefilter = datetime.today() - timedelta(days)
    for reading in SensorReading.objects(date__gt=datefilter)[:3600]:
        #TODO: Create resource_fields for returning a list of dictionaries from a list of reading objects 
        data = reading._data
        reading_id = data.pop('readingid')
        data['date']=str(data.pop('date').isoformat())
        readings[reading_id]=data
    
    return readings

def last_reading():
    
    data = SensorReading.objects.first()._data
    data['date']=str(data.pop('date').isoformat())
    
    return data 

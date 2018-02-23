from mongoengine import connect, Document, StringField, FloatField, DateTimeField, ReferenceField, queryset_manager, CASCADE
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
    name = StringField(max_length=50, required=True, unique=True)
    room = StringField(max_length=50, required=True)
    

class SensorReading(Document):
    sensor = ReferenceField(Sensor, reverse_delete_rule=CASCADE)
    date =  DateTimeField(required=True)
    readingid = StringField(max_length=50, primary_key=True, required=True)

    meta = {'allow_inheritance': True}

    @queryset_manager
    def order_by_date(doc_cls, queryset):
        return queryset.order_by('-date')


# This class will be moved into the sensor specific Blueprint 
class ThermHygReading(SensorReading):
    temperature = FloatField(required=True)
    humidity =  FloatField(required=True)


# The following methods query the entire database for Readings. These will need refactoring, and located in the sensor specific Bluewprints.

def return_all():
    readings = {}
    for reading in SensorReading.objects:
        data = reading._data
        reading_id = data.pop('readingid')
        data['date']=str(data.pop('date').isoformat())
        readings[reading_id]=data
    
    return readings

def return_all_by_date(days, name):
    readings = {}
    datefilter = datetime.today() - timedelta(days)
    sensor = Sensor.objects(name=name).first()
    if sensor:
        for reading in SensorReading.objects(date__gt=datefilter)[:3600].filter(sensor=sensor):
            data = reading._data
            reading_id = data.pop('readingid')
            data['date']=str(data.pop('date').isoformat())
            readings[reading_id]=data
        return readings

    else: 
        return None

def last_reading():
    return SensorReading.order_by_date().first()._data

def get_sensor_name_from_readingid(readingid):
    return SensorReading.objects(readingid=readingid).first().sensor.name

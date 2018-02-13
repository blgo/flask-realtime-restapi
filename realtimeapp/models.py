from mongoengine import connect, Document, StringField, FloatField, DateTimeField
from datetime import datetime, timedelta

# Sensor dictionary for temperature/humidity reading
# THERMOHYGRO = {
#     <string:RoomNameYYYYMMDDHHmmss> : { 'date': <datetime.isoformat>,
#                                         'room': <string: room name>,
#                                         'temperature': <int:Celcius>,
#                                         'humidity': <int> },
#     (...)
# }

# Defining a Document
class SensorReading(Document):
    #TODO: Create resource_fields for returning a list of dictionaries from a list of reading objects 
    #Then, we could save date as a datetime object
    date =  DateTimeField(required=True)
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
     


from nose.tools import assert_equal, assert_raises
import datetime
from utils import TestDbUtils
from realtimeapp.models import return_all, return_all_by_date, ThermHygReading, last_reading, Sensor

test_database = TestDbUtils()
reading_type_sample = {
    'reading1' : {'sample' : 1}
}

def test_sensor_reading_save():
    '''
    Test models using MongoDB
    Create and Read data
    '''
    db_reading1 = test_database.reading_1_doc

    assert_equal(db_reading1.sensor.room, 'backyard_test')
    assert_equal(db_reading1.temperature, 15)
    assert_equal(db_reading1.humidity, 99)
    assert_equal(db_reading1.date, test_database.reading_1.date)

    db_reading2 =  test_database.reading_2_doc

    assert_equal(db_reading2.sensor.room, 'backyard_test')
    assert_equal(db_reading2.temperature, 11.1)
    assert_equal(db_reading2.humidity, 51.5)
    assert_equal(db_reading2.date, test_database.reading_2.date)


def test_sensor_reading_validation_error():
    '''
    Test validation ThermHygReading
    '''
    
    with assert_raises(Exception) as e:
        test_database.reading_3.save()

    assert_equal(e.exception._message,'ValidationError (SensorReading.ThermHygReading:backyard_test_1234567859abe) ') 


def test_return_all():
    '''
    Creates a database dump, used for numpy
    Check that the structure returned by this method is equal to:
    readings = {
        'bedroom20181815170112298831': 
        {'date': '2018-01-15 17:18:12.298831', 'room': 'bedroom', 'temperature': 20, 'humidity': 60},
        'bedroom20181815170113326091': 
        {'date': '2018-01-15 17:18:13.326091', 'room': 'bedroom', 'temperature': 11, 'humidity': 61}, 
        'bedroom20181815170114343102':
        {'date': '2018-01-15 17:18:14.343102', 'room': 'bedroom', 'temperature': 17, 'humidity': 57},
        readingid : {reading._data}
    }
    '''

    readings = return_all()

    assert_equal(type(readings), type(reading_type_sample))
    assert_equal(readings.get('backyard_test_1234567859abc')['humidity'],99) 


def test_return_all_by_date():
    test_sensor_reading_save()
    readings = return_all_by_date(days=1,name='Thermohydrometer')
    
    # Make sure we get the readings are already serialized as a dictionary
    assert_equal(type(readings), type(reading_type_sample))
    # Verify that the data is in the results set (<24h)
    assert_equal(readings.get('backyard_test_1234567859abd')['humidity'],51.5)
    # Verify that the data is NOT in the results set (>24h)
    assert_equal(readings.get('backyard_test_1234567859abf', None), None)


def test_nested_fields():
    assert_equal(test_database.reading_4_doc.sensor.name, "Thermohydrometer")

def test_order_by_date():
    last_reading_from_sample = test_database.reading_2
    assert_equal(ThermHygReading.order_by_date().first(),last_reading_from_sample)

def test_last_reading():
    last_date_from_sample = test_database.reading_2.date
    assert_equal(last_reading()['date'].isoformat(),last_date_from_sample)

def test_save_sensor():
    
    assert_equal(test_database.sensor1_doc.name,Sensor.objects(name='Thermohydrometer')[0].name)


def test_delete_sensor():

    # Check that the sensor readings exist for Thermohydrometer
    assert_equal(ThermHygReading.objects(sensor=test_database.sensor1_doc).first().sensor.name,"Thermohydrometer")

    # Delete sensor
    test_database.sensor1_doc.delete()

    # Try to retrieve Thermohydrometer from database, it shouldn't exist 
    assert not Sensor.objects(name='Thermohydrometer')

    # delete reference fields using CASCADE is enabled, 
    # all readings referencing that sensor are deleted
    assert not ThermHygReading.objects(sensor=test_database.sensor1_doc)
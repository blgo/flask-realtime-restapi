from realtimeapp.models import SensorReading
from nose.tools import assert_equal, assert_raises


def test_sensor_reading_save():
    '''
    Test models using MongoDB
    Create and Read a new datapoint 
    A Mongo database should be running to test this:
    $ docker run --rm -p 27017:27017 -d mongo:3.6.2
    '''

    # Saving Documents
    reading_1 = SensorReading(
        room='backyard_test',
        temperature=15,
        humidity=99,
        date='2018-01-05T15:48:11.893728+00:00',
        readingid = 'backyard_test_1201801051548'
    )
    reading_1.save()       # This will perform an insert

    reading_2 = SensorReading(
        room='backyard_test_2',
        temperature=11.1,
        humidity=51.5,
        date='2018-01-05T16:50:21.114721+00:00',
        readingid = 'backyard_test_220180105165021'
    )
    reading_2.save()


    assert_equal(reading_1.room, 'backyard_test')
    assert_equal(reading_1.temperature, 15)
    assert_equal(reading_1.humidity, 99)
    assert_equal(reading_1.date, '2018-01-05T15:48:11.893728+00:00')

    assert_equal(reading_2.room, 'backyard_test_2')
    assert_equal(reading_2.temperature, 11.1)
    assert_equal(reading_2.humidity, 51.5)
    assert_equal(reading_2.date, '2018-01-05T16:50:21.114721+00:00')

def test_sensor_reading_validation_error():
    '''
    Test validation, validation should be triggered and save command fail
    '''
    reading_3 = SensorReading(
        room='backyard_test_3',
        temperature='string',
        humidity=51.5,
        date='2018-01-05T16:50:21.114721+00:00',
        readingid = 'backyard_test_3201801051650'
    )
    
    with assert_raises(Exception) as e:
        reading_3.save()

    assert_equal(e.exception._message,'ValidationError (SensorReading:backyard_test_3201801051650) ') 
